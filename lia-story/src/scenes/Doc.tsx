import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {Avatar, KLI_MM2, LIA_LOOK} from '../three/Avatar';
import {Cam, ease, lerp3, range, V3} from '../three/cam';
import {Sparkles, Spotlight} from '../three/Props';
import {Env, Stage} from '../three/World';
import {FPS} from '../timeline';
import {AppHome, GamePage, Loading} from '../ui/App';
import {DOC_FONT, UI_FONT} from '../ui/HUD';
import {rand} from '../three/textures';
import {withShake} from './shots';

const VOID: Env = {
	skyTop: '#04020a',
	skyHorizon: '#120614',
	sunDir: [0.3, 1, 0.4],
	sunColor: '#ff99cc',
	sunIntensity: 0.15,
	hemiSky: '#323',
	hemiGround: '#000',
	hemiIntensity: 0.25,
	fog: ['#06030a', 20, 70],
	sunGlow: 0,
};

export const Letterbox: React.FC<{h?: number}> = ({h = 120}) => (
	<>
		<div style={{position: 'absolute', left: 0, right: 0, top: 0, height: h, background: '#000'}} />
		<div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: h, background: '#000'}} />
	</>
);

export const Grain: React.FC<{t: number; opacity?: number}> = ({t, opacity = 0.08}) => (
	<AbsoluteFill
		style={{
			opacity,
			backgroundImage: `repeating-radial-gradient(circle at ${(rand(Math.floor(t * 24)) * 100).toFixed(1)}% ${(rand(Math.floor(t * 24) + 3) * 100).toFixed(1)}%, rgba(255,255,255,0.5) 0, rgba(0,0,0,0.5) 1px, transparent 2px, transparent 3px)`,
			mixBlendMode: 'overlay',
		}}
	/>
);

export const Vignette: React.FC<{amt?: number}> = ({amt = 0.75}) => (
	<AbsoluteFill style={{background: `radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,${amt}) 100%)`}} />
);

// ---------------------------------------------------------------- cold open
export const ColdOpen: React.FC = () => {
	const frame = useCurrentFrame();
	const t = frame / FPS;
	const k = ease(range(t, 0, 7.5));
	const cam: Cam = {pos: lerp3([0.2, 5.0, 6.6], [4.5, 4.4, 14], k), target: lerp3([-1.3, 4.6, 0], [-3.4, 3.4, 0], k), fov: 40};
	const dust = new Array(40).fill(0).map((_, i) => [(rand(i) - 0.5) * 14, (rand(i + 1) * 10 + t * 0.3 * (0.5 + rand(i + 2))) % 10, (rand(i + 3) - 0.5) * 10] as V3);
	const title = range(t, 1.0, 1.6);
	const sub = range(t, 3.2, 3.8);
	const out = range(t, 7.0, 7.5);
	return (
		<AbsoluteFill style={{background: '#000'}}>
			<Stage cam={cam} env={VOID}>
				<mesh position={[0, -0.25, 0]} receiveShadow>
					<cylinderGeometry args={[4, 4.3, 0.5, 48]} />
					<meshStandardMaterial color="#2a1f2c" roughness={0.3} metalness={0.4} />
				</mesh>
				<Spotlight position={[0, 22, 3]} target={[0, 0, 0]} intensity={1600} color="#ffe6f2" />
				<pointLight position={[-6, 4, -6]} color="#ff3d8b" intensity={70} distance={30} />
				<pointLight position={[2, 4.5, 7]} color="#ffd9e8" intensity={22} distance={16} />
				<Avatar look={LIA_LOOK} position={[0, 0, 0]} rotationY={0.25} pose={{time: t, headYaw: -0.5 + ease(range(t, 2.0, 3.2)) * 0.6}} />
				<Sparkles points={dust} t={t} color="#a88aa8" size={0.05} />
			</Stage>
			<Vignette />
			<div style={{position: 'absolute', left: 150, top: 330, opacity: title, transform: `translateX(${(1 - title) * -40}px)`}}>
				<div style={{fontFamily: DOC_FONT, fontSize: 300, color: '#fff', letterSpacing: 40, lineHeight: 1}}>LIA</div>
				<div style={{height: 4, width: 520 * title, background: '#ff4fa3', marginTop: 10}} />
				<div style={{fontFamily: UI_FONT, fontSize: 40, color: '#d8d8d8', marginTop: 24, letterSpacing: 10, opacity: sub, fontWeight: 600}}>
					A MURDER MYSTERY LOVE STORY
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
	const homePress = t > 9.1 && t < 9.35 ? 1 : 0;
	const playPress = t > 11.3 && t < 11.55 ? 1 : 0;
	return (
		<AbsoluteFill style={{background: '#111216'}}>
			{t < 9.6 ? <AppHome t={t - t0} press={homePress} /> : null}
			{t >= 9.3 && t < 11.9 ? <GamePage t={t - 9.3} press={playPress} /> : null}
			{t >= 11.6 ? <Loading t={t - 11.6} /> : null}
			<AbsoluteFill style={{background: '#000', opacity: Math.max(1 - range(t, t0, t0 + 0.25), range(t, 13.7, 14))}} />
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------- end card (+ kli post-credit)
export const EndCard: React.FC<{t0: number}> = ({t0}) => {
	const frame = useCurrentFrame();
	const t = t0 + frame / FPS;
	const lt = t - t0;
	const fadeOut = range(t, 135.9, 136.5);
	const by = range(t, 133.4, 134.0);
	const soon = range(t, 134.0, 134.6);
	const letters = ['L', 'I', 'A'];
	const post = t > 136.8;
	const pt = t - 136.8;
	const kliCam: Cam = withShake(
		{pos: lerp3([0, 4.75, 4.2], [0, 4.7, 3.4], ease(range(t, 136.8, 139.6))), target: [0, 4.65, 0], fov: 38},
		t,
		t > 137.4 && t < 138.2 ? 0.06 * (1 - (t - 137.4) / 0.8) : 0,
	);
	return (
		<AbsoluteFill style={{background: '#000'}}>
			{!post ? (
				<AbsoluteFill style={{opacity: 1 - fadeOut}}>
					<div style={{position: 'absolute', left: 0, right: 0, top: 250, display: 'flex', justifyContent: 'center', gap: 40}}>
						{letters.map((l, i) => {
							const k = ease(range(lt, 0.2 + i * 0.25, 0.6 + i * 0.25));
							return (
								<div
									key={l}
									style={{
										fontFamily: DOC_FONT,
										fontSize: 320,
										lineHeight: 1,
										color: '#fff',
										opacity: k,
										transform: `translateY(${(1 - k) * -80}px) scale(${1.3 - 0.3 * k})`,
										textShadow: '0 0 50px rgba(255,79,163,0.55)',
									}}
								>
									{l}
								</div>
							);
						})}
					</div>
					<div style={{position: 'absolute', left: '50%', top: 590, width: 560 * ease(range(lt, 1.0, 1.6)), height: 5, background: '#ff4fa3', transform: 'translateX(-50%)'}} />
					<div style={{position: 'absolute', left: 0, right: 0, top: 620, textAlign: 'center', fontFamily: UI_FONT, fontSize: 38, letterSpacing: 14, color: '#cfcfcf', opacity: by, fontWeight: 600}}>
						A STORY BY LOJJKLI
					</div>
					<div
						style={{
							position: 'absolute',
							left: 0,
							right: 0,
							top: 700,
							textAlign: 'center',
							fontFamily: DOC_FONT,
							fontSize: 110,
							letterSpacing: 18,
							color: '#ff8fd0',
							opacity: soon,
							transform: `scale(${1.08 - 0.08 * soon})`,
						}}
					>
						COMING SOON
					</div>
				</AbsoluteFill>
			) : (
				<AbsoluteFill style={{opacity: interpolate(pt, [0, 0.3, 2.4, 2.8], [0, 1, 1, 0], {extrapolateRight: 'clamp'})}}>
					<Stage cam={kliCam} env={VOID}>
						<Spotlight position={[2, 10, 6]} target={[0, 4.5, 0]} intensity={700} color="#c9b8ff" />
						<pointLight position={[-3, 5, 3]} color="#ff3d8b" intensity={20} distance={12} />
						<Avatar look={KLI_MM2} position={[0, 0, 0]} pose={{time: t}} />
					</Stage>
					<Vignette amt={0.9} />
				</AbsoluteFill>
			)}
			<Grain t={t} opacity={0.06} />
			<Letterbox />
		</AbsoluteFill>
	);
};
