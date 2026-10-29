import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {Avatar, REQ_LOOK} from '../three/Avatar';
import {Cam, ease, lerp3, range} from '../three/cam';
import {Sparkles, Spotlight} from '../three/Props';
import {Env, Stage} from '../three/World';
import {FPS} from '../timeline';
import {AppHome, GamePage, Loading} from '../ui/App';
import {DiamondIcon, DOC_FONT, UI_FONT} from '../ui/HUD';
import {rand} from '../three/textures';
import {SYMBOLS} from '../three/textures';

const VOID: Env = {
	skyTop: '#020308',
	skyHorizon: '#0a0d18',
	sunDir: [0.3, 1, 0.4],
	sunColor: '#8899ff',
	sunIntensity: 0.15,
	hemiSky: '#223',
	hemiGround: '#000',
	hemiIntensity: 0.25,
	fog: ['#05060c', 20, 70],
	sunGlow: 0,
};

const Letterbox: React.FC<{h?: number}> = ({h = 120}) => (
	<>
		<div style={{position: 'absolute', left: 0, right: 0, top: 0, height: h, background: '#000'}} />
		<div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: h, background: '#000'}} />
	</>
);

const Grain: React.FC<{t: number; opacity?: number}> = ({t, opacity = 0.08}) => (
	<AbsoluteFill
		style={{
			opacity,
			backgroundImage: `repeating-radial-gradient(circle at ${(rand(Math.floor(t * 24)) * 100).toFixed(1)}% ${(rand(Math.floor(t * 24) + 3) * 100).toFixed(1)}%, rgba(255,255,255,0.5) 0, rgba(0,0,0,0.5) 1px, transparent 2px, transparent 3px)`,
			mixBlendMode: 'overlay',
		}}
	/>
);

const Vignette: React.FC = () => <AbsoluteFill style={{background: 'radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,0.75) 100%)'}} />;

// ---------------------------------------------------------------- cold open
export const ColdOpen: React.FC = () => {
	const frame = useCurrentFrame();
	const t = frame / FPS;
	const k = ease(range(t, 0, 7));
	const cam: Cam = {pos: lerp3([0.2, 5.1, 6.8], [4.5, 4.4, 14], k), target: lerp3([-1.3, 4.6, 0], [-3.4, 3.4, 0], k), fov: 40};
	const dust = new Array(40).fill(0).map((_, i) => [
		(rand(i) - 0.5) * 14,
		((rand(i + 1) * 10 + t * 0.3 * (0.5 + rand(i + 2))) % 10),
		(rand(i + 3) - 0.5) * 10,
	] as [number, number, number]);
	const title = range(t, 1.0, 1.6);
	const sub = range(t, 3.1, 3.7);
	const out = range(t, 6.6, 7.0);
	return (
		<AbsoluteFill style={{background: '#000'}}>
			<Stage cam={cam} env={VOID}>
				<mesh position={[0, -0.25, 0]} receiveShadow>
					<cylinderGeometry args={[4, 4.3, 0.5, 48]} />
					<meshStandardMaterial color="#20232c" roughness={0.3} metalness={0.4} />
				</mesh>
				<Spotlight position={[0, 22, 3]} target={[0, 0, 0]} intensity={1600} color="#fff1d6" />
				<pointLight position={[-6, 4, -6]} color="#3d6bff" intensity={60} distance={30} />
				<Avatar look={REQ_LOOK} position={[0, 0, 0]} rotationY={0.25} pose={{time: t, headYaw: -0.5 + ease(range(t, 2.0, 3.2)) * 0.6}} />
				<Sparkles points={dust} t={t} color="#8a8fa8" size={0.05} />
			</Stage>
			<Vignette />
			<div style={{position: 'absolute', left: 150, top: 330, opacity: title, transform: `translateX(${(1 - title) * -40}px)`}}>
				<div style={{fontFamily: DOC_FONT, fontSize: 300, color: '#fff', letterSpacing: 40, lineHeight: 1}}>REQ</div>
				<div style={{height: 4, width: 520 * title, background: '#ffcc33', marginTop: 10}} />
				<div style={{fontFamily: UI_FONT, fontSize: 40, color: '#d8d8d8', marginTop: 24, letterSpacing: 10, opacity: sub, fontWeight: 600}}>
					THE BOY WHO SAID &ldquo;ONE MORE&rdquo;
				</div>
			</div>
			<Grain t={t} />
			<Letterbox h={110 * (1 - out)} />
			<AbsoluteFill style={{background: '#000', opacity: Math.max(1 - t / 0.8, out)}} />
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------- app
export const AppScene: React.FC<{t0: number}> = ({t0}) => {
	const frame = useCurrentFrame();
	const t = t0 + frame / FPS;
	const homePress = t > 8.8 && t < 9.05 ? 1 : 0;
	const playPress = t > 11.1 && t < 11.35 ? 1 : 0;
	return (
		<AbsoluteFill style={{background: '#111216'}}>
			{t < 9.4 ? <AppHome t={t - t0} press={homePress} /> : null}
			{t >= 9.0 && t < 11.7 ? <GamePage t={t - 9.0} press={playPress} /> : null}
			{t >= 11.4 ? <Loading t={t - 11.4} /> : null}
			<AbsoluteFill style={{background: '#000', opacity: 1 - range(t, t0, t0 + 0.25)}} />
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------- end card
const ReelLetter: React.FC<{letter: string; t: number; stop: number}> = ({letter, t, stop}) => {
	const items = [...SYMBOLS.slice(0, 5), letter];
	const h = 300;
	const k = range(t, 0, stop);
	const pos = (1 - Math.pow(1 - k, 3)) * (items.length * 3 - 1);
	const idx = pos;
	return (
		<div style={{width: 230, height: h, overflow: 'hidden', position: 'relative'}}>
			{new Array(items.length * 3).fill(0).map((_, i) => {
				const y = (i - idx) * h;
				if (Math.abs(y) > h * 1.2) return null;
				const it = items[i % items.length];
				const isLetter = it === letter && i === items.length * 3 - 1;
				return (
					<div
						key={i}
						style={{
							position: 'absolute',
							left: 0,
							right: 0,
							top: y,
							height: h,
							display: 'flex',
							alignItems: 'center',
							justifyContent: 'center',
							fontFamily: isLetter ? DOC_FONT : '"Noto Color Emoji", ' + DOC_FONT,
							fontSize: isLetter ? 300 : 150,
							color: '#fff',
							background: isLetter ? 'transparent' : undefined,
							filter: k < 1 ? `blur(${(1 - k) * 4}px)` : undefined,
							textShadow: isLetter ? '0 0 40px rgba(255,204,51,0.5)' : undefined,
						}}
					>
						{it}
					</div>
				);
			})}
		</div>
	);
};

export const EndCard: React.FC<{t0: number}> = ({t0}) => {
	const frame = useCurrentFrame();
	const t = t0 + frame / FPS;
	const lt = t - t0;
	const fadeOut = range(t, 98.0, 98.6);
	const by = range(t, 95.0, 95.6);
	const soon = range(t, 95.6, 96.2);
	return (
		<AbsoluteFill style={{background: '#000'}}>
			<AbsoluteFill style={{opacity: 1 - fadeOut}}>
				<div style={{position: 'absolute', left: 0, right: 0, top: 260, display: 'flex', justifyContent: 'center', gap: 10}}>
					<ReelLetter letter="R" t={lt - 0.2} stop={1.0} />
					<ReelLetter letter="E" t={lt - 0.2} stop={1.3} />
					<ReelLetter letter="Q" t={lt - 0.2} stop={1.6} />
				</div>
				<div style={{position: 'absolute', left: 0, right: 0, top: 590, textAlign: 'center', fontFamily: UI_FONT, fontSize: 38, letterSpacing: 14, color: '#cfcfcf', opacity: by, fontWeight: 600}}>
					A STORY BY LOJJKLI
				</div>
				<div
					style={{
						position: 'absolute',
						left: 0,
						right: 0,
						top: 680,
						textAlign: 'center',
						fontFamily: DOC_FONT,
						fontSize: 110,
						letterSpacing: 18,
						color: '#ffcc33',
						opacity: soon,
						transform: `scale(${1.08 - 0.08 * soon})`,
					}}
				>
					COMING SOON
				</div>
			</AbsoluteFill>
			{/* post-credit: one more... */}
			{t > 98.8 && t < 101.4 ? (
				<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', opacity: interpolate(t, [98.8, 99.2, 101.0, 101.4], [0, 1, 1, 0])}}>
					<div style={{display: 'flex', alignItems: 'center', gap: 18, fontFamily: '"Fredoka", sans-serif', fontWeight: 700, fontSize: 70, color: '#ff5757'}}>
						<DiamondIcon size={80} /> 0
					</div>
				</AbsoluteFill>
			) : null}
			<Grain t={t} opacity={0.06} />
			<Letterbox />
		</AbsoluteFill>
	);
};
