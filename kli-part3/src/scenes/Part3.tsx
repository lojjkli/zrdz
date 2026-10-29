import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {Avatar, KLI_DEEP, KLI_RICH, MYNINN_LOOK, npcLook} from '../three/Avatar';
import {Cam, ease, lerp, lerp3, range, V3} from '../three/cam';
import {LampPost, Sparkles, Spotlight} from '../three/Props';
import {Clouds, Env, lerpEnv, Stage} from '../three/World';
import {Lobby, LOBBY_DAY, LOBBY_NIGHT, LOBBY_SUNSET} from '../three/MM2World';
import {baseplateTexture, Bread, CashRain, DefaultCube, GoldChair, GoldMansion, Pigeon, TalkingDonut, TeaTray, ViewportGrid} from '../three/KliProps';
import {rand} from '../three/textures';
import {bubbleOf, FPS, HATERS, RENDER_FAST, SUN_BACK, SUN_GRAB, talking} from '../timeline';
import {Billboards, BB} from '../ui/Billboards';
import {DOC_FONT, UI_FONT} from '../ui/HUD';
import {BigText, GameUI} from '../ui/MM2';
import {BlenderUI, Fade, Flash, PopWords, RobuxCounter} from '../ui/KliUI';
import {Grain, Letterbox, Vignette} from './Doc';
import {face, Shot, shotAt, withShake} from './shots';

const VOID: Env = {
	skyTop: '#04020a',
	skyHorizon: '#0c0a1c',
	sunDir: [0.3, 1, 0.4],
	sunColor: '#b8a8ff',
	sunIntensity: 0.15,
	hemiSky: '#334',
	hemiGround: '#000',
	hemiIntensity: 0.25,
	fog: ['#05040c', 20, 70],
	sunGlow: 0,
};
const VIEWPORT: Env = {
	skyTop: '#3d3d3d',
	skyHorizon: '#3d3d3d',
	skyBottom: '#3d3d3d',
	sunDir: [0.4, 1, 0.6],
	sunColor: '#ffffff',
	sunIntensity: 2.0,
	hemiSky: '#ffffff',
	hemiGround: '#444',
	hemiIntensity: 1.0,
	fog: ['#3d3d3d', 400, 900],
	sunGlow: 0,
};
const DARK: Env = {...LOBBY_NIGHT, sunIntensity: 0.25, hemiIntensity: 0.3, skyTop: '#000', skyHorizon: '#0a0d18', fog: ['#0a0d18', 40, 160]};
const Y = 0.4;

const Grass: React.FC = () => (
	<mesh position={[0, -0.5, 0]} receiveShadow>
		<boxGeometry args={[600, 1, 600]} />
		<meshStandardMaterial map={baseplateTexture('richgrass', '#4f9a3a', '#468a33', 140)} roughness={0.9} />
	</mesh>
);
const HILL_TOP: V3 = [-90, 10, -150];
const Hill: React.FC = () => (
	<mesh position={[HILL_TOP[0], -16, HILL_TOP[2]]} receiveShadow>
		<sphereGeometry args={[26, 32, 16]} />
		<meshStandardMaterial color="#3f8a32" roughness={0.95} />
	</mesh>
);
const SUN_POS: V3 = [60, 70, -160];
const SkySun: React.FC<{p: V3; r?: number}> = ({p, r = 10}) => (
	<group position={p}>
		<mesh>
			<sphereGeometry args={[r, 24, 16]} />
			<meshBasicMaterial color="#fff2a0" fog={false} />
		</mesh>
		<mesh>
			<sphereGeometry args={[r * 1.5, 24, 16]} />
			<meshBasicMaterial color="#ffd84d" transparent opacity={0.25} fog={false} depthWrite={false} />
		</mesh>
		<pointLight color="#ffe08a" intensity={r * 40} distance={r * 10} decay={1.2} />
	</group>
);

/** Binocular mask (two circles) */
const Binoculars: React.FC<{o: number}> = ({o}) =>
	o <= 0 ? null : (
		<AbsoluteFill style={{opacity: o}}>
			<svg width={1920} height={1080}>
				<defs>
					<mask id="bino">
						<rect width={1920} height={1080} fill="#fff" />
						<circle cx={740} cy={540} r={400} fill="#000" />
						<circle cx={1180} cy={540} r={400} fill="#000" />
					</mask>
				</defs>
				<rect width={1920} height={1080} fill="#000" mask="url(#bino)" />
			</svg>
		</AbsoluteFill>
	);

// ================================================================ cold open
export const ColdOpen3: React.FC = () => {
	const t = useCurrentFrame() / FPS;
	const k = ease(range(t, 0, 8));
	const cam: Cam = {pos: lerp3([1.4, 5.0, 10], [3.8, 4.6, 15], k), target: lerp3([0.4, 4.4, 0], [-1.6, 4.0, 0], k), fov: 42};
	const eyes = t > 2.4 && !(t > 3.4 && t < 3.55);
	const title = range(t, 4.4, 4.9);
	const sub = range(t, 5.2, 5.8);
	const out = range(t, 7.5, 8);
	return (
		<AbsoluteFill style={{background: '#000'}}>
			<Stage cam={cam} env={VOID}>
				<mesh position={[0, -0.25, 0]} receiveShadow>
					<cylinderGeometry args={[5, 5.3, 0.5, 48]} />
					<meshStandardMaterial color="#1f1f2c" roughness={0.3} metalness={0.4} />
				</mesh>
				<Spotlight position={[0, 22, 3]} target={[0, 0, 0]} intensity={1600} color="#e6e6ff" />
				<pointLight position={[2, 5, 7]} color="#e0dcff" intensity={30} distance={16} />
				<Avatar look={KLI_DEEP} position={[-1, 0, 0]} rotationY={0.25} pose={{time: t}} />
				<TalkingDonut position={[2.6, 0, 0.2]} scale={1.1} yaw={-0.3} t={t} mood="happy" bowtie />
				{eyes
					? [-1, 1].map((s) => (
							<mesh key={s} position={[-3 + s * 1.4, 10, -16]}>
								<sphereGeometry args={[0.35, 12, 10]} />
								<meshBasicMaterial color="#ff3a1a" fog={false} />
							</mesh>
					  ))
					: null}
			</Stage>
			<Vignette />
			<div style={{position: 'absolute', left: 120, top: 90, fontFamily: DOC_FONT, fontSize: 80, letterSpacing: 16, color: '#d8d8ff', opacity: interpolate(t, [0.4, 0.8, 3.6, 4.0], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}}>
				LAST TIME...
			</div>
			<div style={{position: 'absolute', left: 150, top: 330, opacity: title, transform: `translateX(${(1 - title) * -40}px)`}}>
				<div style={{fontFamily: DOC_FONT, fontSize: 300, color: '#fff', letterSpacing: 40, lineHeight: 1}}>KLI 3</div>
				<div style={{height: 4, width: 640 * title, background: '#a9b4c4', marginTop: 10}} />
				<div style={{fontFamily: UI_FONT, fontSize: 40, color: '#d8d8d8', marginTop: 24, letterSpacing: 10, opacity: sub, fontWeight: 600}}>THE PIGEON</div>
			</div>
			<Grain t={t} />
			<Letterbox h={110 * (1 - out)} />
			<AbsoluteFill style={{background: '#000', opacity: Math.max(1 - t / 0.7, out)}} />
		</AbsoluteFill>
	);
};

// ================================================================ peaceful life, then the sun gets stolen, then the plan
const DONUT_P: V3 = [3.2, 0, 2.2];
const MY_P: V3 = [-4.2, 0, 2.5];
const pigeonSky = (t: number): V3 => {
	if (t < SUN_GRAB) return lerp3([-150, 60, -120], [SUN_POS[0], SUN_POS[1] + 10, SUN_POS[2]], range(t, 38.4, SUN_GRAB));
	return lerp3([SUN_POS[0], SUN_POS[1] + 10, SUN_POS[2]], [260, 110, -220], range(t, SUN_GRAB, 42.4));
};

const LAWN_SHOTS: Shot[] = [
	{from: 8, to: 13.2, cam: (t, k) => ({pos: lerp3([12, 7, 17], [10, 6.5, 15], k), target: [0, 3, -1], fov: 48})},
	{from: 13.2, to: 15.2, cam: () => ({pos: [7.6, 3.6, 6.2], target: [DONUT_P[0], 2.4, DONUT_P[2]], fov: 44})},
	{from: 15.2, to: 17.6, cam: () => ({pos: [0.6, 4.4, 5.6], target: [0, 4.0, 0], fov: 42})},
	{from: 17.6, to: 22, cam: (t, k) => ({pos: [-24, 6, 10], target: [HILL_TOP[0], HILL_TOP[1] + 2, HILL_TOP[2]], fov: lerp(14, 8, ease(k))})},
	// sun
	{from: 38, to: 42.6, cam: () => ({pos: [8, 3, 26], target: [30, 42, -110], fov: 62})},
	{from: 42.6, to: 46, cam: (t, k) => ({pos: lerp3([1.0, 5.4, 7.2], [0.8, 5.3, 6.4], k), target: [0, 4.9, 0], fov: 42})},
	{from: 46, to: 48.6, cam: () => ({pos: [MY_P[0] + 1.4, 5.2, MY_P[2] + 5], target: [MY_P[0], 4.6, MY_P[2]], fov: 42})},
	{from: 48.6, to: 52, cam: (t, k) => ({pos: lerp3([12, 9, 18], [10, 8, 16], k), target: [0, 3, 0], fov: 50})},
	// plan
	{from: 52, to: 56.6, cam: (t, k) => ({pos: lerp3([10, 7, 15], [8, 6.5, 13], k), target: [0, 3, 1], fov: 48})},
	{from: 56.6, to: 59.4, cam: () => ({pos: [5.5, 2.8, 8.5], target: [DONUT_P[0], 2.5, DONUT_P[2]], fov: 44})},
	{from: 59.4, to: 64, cam: (t, k) => ({pos: lerp3([1.0, 5.4, 7.2], [0.7, 5.2, 6.0], k), target: [0, 4.9, 0], fov: 42})},
];

export const LawnScene: React.FC<{t0: number; mode: 'peace' | 'sun' | 'plan'}> = ({t0, mode}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const cam = withShake(shotAt(LAWN_SHOTS, t).cam, t, mode === 'sun' && t > SUN_GRAB && t < SUN_GRAB + 0.8 ? 0.06 : 0);
	const dark = mode === 'peace' ? 0 : mode === 'sun' ? range(t, SUN_GRAB + 0.2, SUN_GRAB + 2.0) : 1;
	const env = lerpEnv({...LOBBY_DAY, sunDir: [0.4, 0.45, -0.9]}, DARK, dark);
	const sitting = mode === 'peace';
	const kTalk = talking('kli', t);
	const dTalk = talking('donut', t);
	const pg = pigeonSky(t);
	const sunP: V3 = mode === 'sun' && t >= SUN_GRAB ? [pg[0], pg[1] - 16, pg[2]] : SUN_POS;
	const sunOn = mode === 'peace' || (mode === 'sun' && t < 42.6);
	const lookUp = mode === 'sun' && t < 46 ? -0.45 : 0;
	const bino = mode === 'peace' ? range(t, 17.6, 17.8) : 0;
	const kliP: V3 = sitting ? [0, 0.25, 0.1] : [0, 0, 0.6];
	const items: BB[] = [
		{p: sitting ? [0, -0.5, 0.1] : kliP, name: 'lojjkli', talking: kTalk, emote: mode === 'plan' ? null : null},
		{p: DONUT_P, h: 4.6, name: 'TheDonut', talking: dTalk, emote: mode === 'plan' ? {char: '💡', age: t - 56.6} : null},
		{p: MY_P, name: 'myninn', talking: talking('myninn', t)},
	];
	return (
		<AbsoluteFill>
			<Stage cam={cam} env={{...env, shadowCenter: [0, 0, -4], shadowSize: 30}}>
				<Grass />
				{dark < 1 ? <Clouds t={t} opacity={0.92 * (1 - dark)} /> : null}
				<Hill />
				<GoldMansion position={[0, 0, -32]} />
				{sitting ? <GoldChair position={[0, 0, 0]} /> : null}
				{sunOn ? <SkySun p={sunP} /> : null}
				{mode !== 'peace' ? <LampPost position={[1.5, 0, 6]} /> : null}
				<Avatar look={KLI_RICH} position={kliP} pose={{time: t, sit: sitting ? 1 : 0, headPitch: lookUp}} />
				<TalkingDonut position={DONUT_P} yaw={-0.35} scale={1.25} t={t} talk={dTalk} mood={mode === 'sun' && t > SUN_GRAB ? 'hurt' : 'happy'} bowtie />
				{sitting ? <TeaTray position={[DONUT_P[0] - 0.6, 2.1, DONUT_P[2] + 1.2]} /> : null}
				<Avatar look={MYNINN_LOOK} position={MY_P} rotationY={face(MY_P, [0, 0, 6])} pose={{time: t + 2, headPitch: lookUp, armsUp: mode === 'sun' && t > 46.2 && t < 48 ? 0.6 : 0}} />
				{/* the pigeon: tiny on the hill, giant in the sky */}
				{mode === 'peace' ? <Pigeon position={[HILL_TOP[0], HILL_TOP[1] + 0.9, HILL_TOP[2]]} rotationY={0.6} t={t} flap={0} scale={3} /> : null}
				{mode === 'sun' && t > 38.4 && t < 42.4 ? <Pigeon position={pg} rotationY={Math.PI / 2} t={t} scale={14} /> : null}
				{mode === 'peace' && t < 17.6 ? <CashRain t={t} center={[0, 0, -4]} area={40} count={70} /> : null}
			</Stage>
			{bino <= 0 ? <Billboards cam={cam} t={t} items={items} /> : null}
			{bino <= 0 ? <GameUI t={t} talking={kTalk} mode="plain" chatFrom={mode === 'sun' ? 46 : 999} /> : null}
			{bino <= 0 ? <RobuxCounter value={999_999_999} gold /> : null}
			<Binoculars o={bino} />
			{mode === 'peace' ? <BigText t={t} from={19.6} to={21.8} text="👀" top={150} size={120} /> : null}
			{mode === 'sun' ? <BigText t={t} from={SUN_GRAB + 0.2} to={SUN_GRAB + 2.2} text="☀️ SUN: STOLEN" color="#ffd84d" top={470} size={100} /> : null}
			{mode === 'plan' ? <BigText t={t} from={60.6} to={63.2} text="🍞 OPERATION: BREAD" color="#ffd28a" top={800} size={96} /> : null}
			<Fade t={t} inAt={t0} inDur={0.5} outFrom={mode === 'peace' ? 21.5 : mode === 'sun' ? 51.6 : 63.5} outTo={mode === 'peace' ? 22 : mode === 'sun' ? 52 : 64} />
		</AbsoluteFill>
	);
};

// ================================================================ the pigeon reveal on the hill
const P_ON_HILL: V3 = [0, 0, 0];
const REVEAL_SHOTS: Shot[] = [
	{from: 22, to: 24.4, cam: (t, k) => ({pos: lerp3([1.6, 2.2, 4.4], [1.4, 2.1, 3.8], k), target: [0, 1.6, 0.6], fov: 34})},
	{from: 24.4, to: 30.4, cam: (t, k) => ({pos: lerp3([6, 3.5, 9], [4.5, 3, 7], k), target: [0, 1.5, 0], fov: 44})},
	{from: 30.4, to: 32.2, cam: (t, k) => ({pos: lerp3([10, 2, 16], [16, 2, 30], ease(range(t, 30.4, 30.9))), target: [0, 10, 0], fov: 58})},
	{from: 32.2, to: 35.5, cam: (t, k) => ({pos: lerp3([6, 1.6, 22], [5, 1.6, 20], k), target: [0, 14, 0], fov: 60})},
	{from: 35.5, to: 38, cam: (t, k) => ({pos: [12, 4, 30], target: [0, 10 + (t - 35.5) * 12, 0], fov: 58})},
];

export const RevealScene: React.FC<{t0: number}> = ({t0}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const shake = (t > 30.4 && t < 31.2 ? 0.25 : 0) + (t > 32.2 && t < 35.5 ? 0.08 : 0);
	const cam = withShake(shotAt(REVEAL_SHOTS, t).cam, t, shake);
	const s = lerp(2, 14, ease(range(t, 30.4, 30.8)));
	const fly = Math.max(0, t - 35.5);
	const p: V3 = [P_ON_HILL[0], P_ON_HILL[1] + 0.3 * s + fly * fly * 8, P_ON_HILL[2]];
	return (
		<AbsoluteFill>
			<Stage cam={cam} env={{...LOBBY_SUNSET, shadowCenter: [0, 0, 0], shadowSize: 30}}>
				<Grass />
				<Clouds t={t} />
				<Pigeon position={p} rotationY={0.3} t={t} flap={t > 35.4 ? 1 : 0} scale={s} />
				<pointLight position={[3, 4, 6]} color="#ffd2b0" intensity={40} distance={30} />
			</Stage>
			<BigText t={t} from={30.4} to={32.0} text="HUGE." color="#ffffff" top={470} size={150} />
			<Flash t={t} at={30.4} dur={0.3} />
			<Fade t={t} inAt={t0} inDur={0.3} outFrom={37.5} outTo={38} />
		</AbsoluteFill>
	);
};

// ================================================================ modeling the bread (and the 440p render)
const RenderWindow: React.FC<{t: number}> = ({t}) => {
	if (t < 68.4) return null;
	const fast = t >= RENDER_FAST;
	const pct = fast ? Math.min(100, 1 + 99 * ease(range(t, RENDER_FAST + 0.2, RENDER_FAST + 1.1))) : t < 71.8 ? 1 : 1 + (t - 71.8) * 0.1;
	const done = pct >= 100;
	return (
		<div style={{position: 'absolute', left: 520, top: 230, width: 820, borderRadius: 12, background: '#2b2b2b', border: '2px solid #1a1a1a', boxShadow: '0 30px 80px rgba(0,0,0,0.7)', fontFamily: UI_FONT, color: '#ddd', overflow: 'hidden'}}>
			<div style={{padding: '12px 18px', background: '#3a3a3a', fontSize: 24, fontWeight: 700}}>Render {fast ? '· 440p' : '· 4K'}</div>
			<div style={{padding: 22}}>
				<div style={{height: 300, borderRadius: 8, background: done ? 'radial-gradient(circle at 50% 55%, #d9a052 0 22%, #a8662a 23% 30%, #3d3d3d 31%)' : '#1d1d1d', filter: done ? 'blur(3px)' : 'none', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 30, color: '#777'}}>
					{done ? '' : '...'}
				</div>
				<div style={{marginTop: 18, height: 34, borderRadius: 8, background: '#1a1a1a', overflow: 'hidden'}}>
					<div style={{width: `${pct}%`, height: '100%', background: done ? '#4fdc6a' : '#4772b3'}} />
				</div>
				<div style={{marginTop: 12, fontSize: 26, display: 'flex', justifyContent: 'space-between'}}>
					<span>{done ? 'DONE ✅' : `Rendering ${Math.floor(pct)}%`}</span>
					<span style={{color: !fast && t > 71.8 ? '#ff6b6b' : '#aaa', fontWeight: 700}}>Time left: {fast ? (done ? '0:00:00' : '0:00:01') : '3:00:00'}</span>
				</div>
			</div>
		</div>
	);
};

export const BreadForge: React.FC<{t0: number}> = ({t0}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const cam: Cam = {pos: lerp3([9, 6, 9], [7.5, 5, 7.5], range(t, 64, 81)), target: [0, 1.6, 0], fov: 44};
	const grow = ease(range(t, 65.6, 67.2));
	return (
		<AbsoluteFill style={{background: '#3d3d3d'}}>
			<Stage cam={cam} env={VIEWPORT}>
				<ViewportGrid />
				<DefaultCube scale={t < 65.6 ? 1 : 0} />
				{grow > 0 ? (
					<group rotation={[0, t * 0.6, 0]}>
						<Bread position={[0, 1.5, 0]} scale={4 * grow} />
					</group>
				) : null}
			</Stage>
			<BlenderUI t={t} outliner={t < 65.6 ? ['Camera', 'Light', 'Cube'] : ['Camera', 'Light', 'BIG_BREAD']} title="bread_FINAL_final.blend" />
			<RenderWindow t={t} />
			<PopWords t={t} until={80.4} words={[{at: RENDER_FAST, text: '440p 🔥', x: 1500, y: 200, rot: 6, color: '#ffd84d'}]} />
			<Fade t={t} inAt={t0} inDur={0.4} outFrom={80.5} outTo={81} />
		</AbsoluteFill>
	);
};

// ================================================================ the bait, the sun comes back, the pet
const BREAD_AT: V3 = [0, Y, -1];
const PIG_AT: V3 = [0, Y, -12];
const PIG_S = 12;
const SUN_SLEEP: V3 = [11, Y + 3, -12];
const HIDE: V3[] = [
	[-9.6, Y, 9],
	[-7.2, Y, 9.6],
	[-12, Y, 9.4],
];
const TRIO_OUT: V3[] = [
	[2, Y, 2],
	[-1.5, Y, 3.5],
	[4.8, Y, 3.5],
];
const trio = (i: number, t: number): V3 => lerp3(HIDE[i], TRIO_OUT[i], range(t, 96.6, 98.4));

const BAIT_SHOTS: Shot[] = [
	{from: 81, to: 84.8, cam: (t, k) => ({pos: lerp3([14, 10, 22], [12, 9, 19], k), target: [0, 3, -2], fov: 48})},
	{from: 84.8, to: 87.0, cam: () => ({pos: [16, 4, 14], target: [0, 8, -10], fov: 56})},
	{from: 87.0, to: 89.6, cam: (t, k) => ({pos: lerp3([4, 8, 8], [3.5, 8.5, 7], k), target: [0, 10, -8], fov: 50})},
	{from: 89.6, to: 91.8, cam: () => ({pos: [12, 6, 8], target: [0, 4, -4], fov: 52})},
	{from: 91.8, to: 96.0, cam: (t, k) => ({pos: lerp3([15, 5, 12], [14, 5, 10], k), target: [0, 4, -9], fov: 50})},
	{from: 96.0, to: 99, cam: (t, k) => ({pos: [-2, 6, 16], target: [0, 4, 2], fov: 50})},
	// sun back
	{from: 99, to: SUN_BACK + 1.6, cam: (t, k) => ({pos: [16, 4, 8], target: lerp3([8, 4, -10], [20, 30, -40], ease(range(t, SUN_BACK, SUN_BACK + 1.6))), fov: 56})},
	{from: SUN_BACK + 1.6, to: 108, cam: (t, k) => ({pos: lerp3([10, 7, 16], [9, 7.5, 15], k), target: [0, 4, -2], fov: 50})},
	// pet
	{from: 108, to: 110.4, cam: (t, k) => ({pos: lerp3([10, 8, 14], [9, 7, 12], k), target: [0, 3, -6], fov: 50})},
	{from: 110.4, to: 115.2, cam: (t, k) => ({pos: lerp3([1.2, 1.7, -4.6], [1.0, 1.6, -5.0], k), target: [0, 1.0, -7.5], fov: 44})},
	{from: 115.2, to: 119, cam: (t, k) => ({pos: [10, 5, -2], target: [0, 3, -4], fov: 46})},
	{from: 119, to: 124, cam: (t, k) => ({pos: lerp3([0.8, 6.0, 4.2], [0.6, 5.9, 3.4], k), target: [0, 5.4, -3.4], fov: 44})},
];

export const LobbyNight: React.FC<{t0: number; mode: 'bait' | 'sunback' | 'pet'}> = ({t0, mode}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const cam = withShake(shotAt(BAIT_SHOTS, t).cam, t, mode === 'bait' && t > 86.6 && t < 87.2 ? 0.2 : 0);
	const day = mode === 'bait' ? 0 : mode === 'sunback' ? range(t, SUN_BACK + 0.8, SUN_BACK + 2.4) : 1;
	const env = lerpEnv(DARK, LOBBY_DAY, day);
	// pigeon
	const land = range(t, 84.8, 86.6);
	const chomps = Math.floor(Math.max(0, Math.min(6, (t - 89.6) / 0.35 + 1)));
	const asleep = mode !== 'pet' ? t > 92.2 : t < 108.6;
	const pigS = mode === 'pet' ? lerp(PIG_S, 1.6, ease(range(t, 108.6, 110.2))) : PIG_S;
	const onHead = mode === 'pet' && t > 119.0;
	const KLI_PET: V3 = [0, Y, -3.4];
	let pigP: V3 = [PIG_AT[0], PIG_AT[1] + 0.3 * pigS + (mode === 'bait' ? (1 - ease(land)) * 40 : 0), PIG_AT[2]];
	if (mode === 'pet') pigP = [0, Y + 0.3 * pigS, lerp(PIG_AT[2], -7.5, range(t, 108.6, 110.2))];
	if (onHead) pigP = lerp3(pigP, [0, Y + 6.0, KLI_PET[2]], ease(range(t, 119.0, 119.8)));
	const bob = mode === 'bait' && t > 89.6 && t < 91.8 ? Math.abs(Math.sin((t - 89.6) * 9)) * 0.5 : 0;
	const pigRot: V3 = asleep ? [0, 0.4, 1.2] : [bob, 0, 0];
	const breadS = mode === 'bait' ? 7 * (1 - chomps / 6) : 0;
	// sun
	const sunUp = mode === 'sunback' ? ease(range(t, SUN_BACK, SUN_BACK + 1.8)) : mode === 'pet' ? 1 : 0;
	const sunP = lerp3(SUN_SLEEP, [80, 90, -200], sunUp);
	const sunR = lerp(3, 10, sunUp);
	const kTalk = talking('kli', t);
	const pTalk = talking('pigeon', t);
	const kp = mode === 'bait' ? trio(0, t) : mode === 'sunback' ? TRIO_OUT[0] : KLI_PET;
	const giving = mode === 'pet' && t > 115.2 && t < 117.6;
	const items: BB[] = [
		{p: kp, name: 'lojjkli', talking: kTalk, hearts: onHead && t > 119.8 ? (t - 119.8) % 2.5 : undefined},
		{p: [pigP[0], pigP[1] - 0.3 * pigS, pigP[2]], h: (asleep ? 0.9 : 1.4) * pigS + 1.0, name: 'THE PIGEON', talking: pTalk, emote: asleep ? {char: '💤', age: (t - 92.2) % 1.5} : null},
	];
	if (mode !== 'pet') items.push({p: mode === 'bait' ? trio(1, t) : TRIO_OUT[1], name: 'myninn'});
	if (mode !== 'pet') items.push({p: mode === 'bait' ? trio(2, t) : TRIO_OUT[2], h: 4.6, name: 'TheDonut'});
	const cheering = mode === 'sunback' && t > 102.8;
	return (
		<AbsoluteFill>
			<Stage cam={cam} env={{...env, shadowCenter: [0, 0, -4], shadowSize: 30}}>
				<Lobby t={t} lampsOn={1 - day} />
				{day > 0 ? <Clouds t={t} opacity={0.92 * day} /> : null}
				{breadS > 0.05 ? <Bread position={[BREAD_AT[0], BREAD_AT[1] + 0.3 * breadS, BREAD_AT[2]]} rotationY={0.3} scale={breadS} /> : null}
				<group position={pigP} rotation={pigRot}>
					<Pigeon position={[0, 0, 0]} rotationY={0} t={t} flap={(mode === 'bait' && land < 1) || (onHead && t < 119.8) ? 1 : 0} scale={onHead ? 0.9 : pigS} />
				</group>
				{mode !== 'pet' || sunUp < 1 ? <SkySun p={sunP} r={sunR} /> : <SkySun p={[80, 90, -200]} r={10} />}
				{mode !== 'pet' ? (
					<>
						<Avatar look={KLI_RICH} position={kp} rotationY={mode === 'bait' && t < 96.6 ? Math.PI * 0.85 : mode === 'sunback' ? -0.6 : Math.PI} pose={{time: t, walk: t * 10, walkAmt: mode === 'bait' && t > 96.6 && t < 98.4 ? 1 : 0, armsUp: (mode === 'sunback' && t > 99.6 && t < SUN_BACK + 0.6) || cheering ? 1 : 0, jump: cheering ? Math.abs(Math.sin(t * 8)) * 0.6 : 0}} />
						<Avatar look={MYNINN_LOOK} position={mode === 'bait' ? trio(1, t) : TRIO_OUT[1]} rotationY={mode === 'bait' && t < 96.6 ? Math.PI * 0.85 : Math.PI} pose={{time: t + 1, walk: t * 10, walkAmt: mode === 'bait' && t > 96.6 && t < 98.4 ? 1 : 0, jump: cheering ? Math.abs(Math.sin(t * 8 + 1)) * 0.6 : 0, armsUp: cheering ? 1 : 0}} />
						<TalkingDonut position={mode === 'bait' ? trio(2, t) : TRIO_OUT[2]} yaw={Math.PI} scale={1.25} t={t} mood="happy" bowtie />
						{mode === 'bait' ? <mesh position={[-9.6, Y + 1.2, 6.6]} castShadow><boxGeometry args={[7, 2.4, 1]} /><meshStandardMaterial color="#6b4a2a" /></mesh> : null}
					</>
				) : (
					<>
						<Avatar look={KLI_RICH} position={KLI_PET} rotationY={t > 118.8 ? 0 : Math.PI} pose={{time: t, point: giving ? 1 : 0}} />
						{giving ? <Bread position={[KLI_PET[0] - 1.5, KLI_PET[1] + 3.9, KLI_PET[2] - 2.0]} scale={0.8} /> : null}
					</>
				)}
				{cheering
					? HATERS.map((h, i) => {
							const p: V3 = [-13 + i * 3, Y, -1];
							return <Avatar key={h.name} look={npcLook([3, 8, 10, 5][i])} position={p} rotationY={Math.PI} pose={{time: t + i, armsUp: 1, jump: Math.abs(Math.sin(t * 8 + i)) * 0.8}} />;
					  })
					: null}
				{mode === 'pet' && t > 108.6 && t < 110.6 ? <Sparkles points={new Array(16).fill(0).map((_, i) => [Math.sin(i * 2.1) * 4 * (t - 108.6), 2 + (i % 4) * 2, -9 + Math.cos(i * 2.1) * 4 * (t - 108.6)] as V3)} t={t} color="#ffffff" size={0.3} /> : null}
				<pointLight position={[0, 8, 6]} color="#cfd8ff" intensity={60 * (1 - day)} distance={30} />
			</Stage>
			<Billboards cam={cam} t={t} items={items} />
			<GameUI t={t} talking={kTalk} mode="plain" chatFrom={mode === 'bait' ? 999 : 100} />
			{mode === 'bait' ? (
				<>
					<BigText t={t} from={89.7} to={91.8} text="CHOMP CHOMP 🍞" color="#ffd28a" top={470} size={100} />
					<BigText t={t} from={96.0} to={97.4} text="NOW!" color="#ff5b5b" top={470} size={150} />
				</>
			) : mode === 'sunback' ? (
				<BigText t={t} from={SUN_BACK + 1.4} to={SUN_BACK + 3.6} text="☀️ SUN: RETURNED" color="#ffd84d" top={470} size={100} />
			) : (
				<BigText t={t} from={120.2} to={123.4} text="🕊️ NEW PET UNLOCKED" color="#ffffff" top={760} size={90} />
			)}
			<Fade t={t} inAt={t0} inDur={mode === 'sunback' ? 0.01 : 0.5} outFrom={mode === 'bait' ? 999 : mode === 'sunback' ? 999 : 123.5} outTo={mode === 'pet' ? 124 : 1000} />
		</AbsoluteFill>
	);
};

// ================================================================ end + the cube
export const EndCard3: React.FC<{t0: number}> = ({t0}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const lt = t - t0;
	const fadeOut = range(t, 129.4, 130);
	const by = range(t, 125.6, 126.2);
	const soon = range(t, 126.2, 126.8);
	const post = t > 130.2;
	const pt = t - 130.2;
	const cubeS = t > 131 ? Math.min(1, (t - 131) / 0.2) * (t > 135.2 ? 1 + (t - 135.2) * 6 : 1) : 0;
	const cam: Cam = withShake({pos: [0.8, 5.0, 8.6], target: [0.8, 4.4, 0], fov: 40}, t, t > 134 && t < 134.6 ? 0.05 : 0);
	return (
		<AbsoluteFill style={{background: '#000'}}>
			{!post ? (
				<AbsoluteFill style={{opacity: 1 - fadeOut}}>
					<div style={{position: 'absolute', left: 0, right: 0, top: 250, display: 'flex', justifyContent: 'center', gap: 40}}>
						{['K', 'L', 'I', '3'].map((l, i) => {
							const k = ease(range(lt, 0.2 + i * 0.25, 0.6 + i * 0.25));
							return (
								<div key={l} style={{fontFamily: DOC_FONT, fontSize: 320, lineHeight: 1, color: i === 3 ? '#a9b4c4' : '#fff', opacity: k, transform: `translateY(${(1 - k) * -80}px) scale(${1.3 - 0.3 * k})`, marginLeft: i === 3 ? 50 : 0}}>
									{l}
								</div>
							);
						})}
					</div>
					<div style={{position: 'absolute', left: '50%', top: 590, width: 620 * ease(range(lt, 1.2, 1.8)), height: 5, background: '#a9b4c4', transform: 'translateX(-50%)'}} />
					<div style={{position: 'absolute', left: 0, right: 0, top: 620, textAlign: 'center', fontFamily: UI_FONT, fontSize: 38, letterSpacing: 14, color: '#cfcfcf', opacity: by, fontWeight: 600}}>A STORY BY LOJJKLI</div>
					<div style={{position: 'absolute', left: 0, right: 0, top: 700, textAlign: 'center', fontFamily: DOC_FONT, fontSize: 110, letterSpacing: 18, color: '#d7dde6', opacity: soon}}>THE TRILOGY</div>
				</AbsoluteFill>
			) : (
				<AbsoluteFill style={{opacity: interpolate(pt, [0, 0.3, 5.3, 5.8], [0, 1, 1, 0], {extrapolateRight: 'clamp'})}}>
					<Stage cam={cam} env={VOID}>
						<Spotlight position={[2, 10, 6]} target={[0.8, 4, 0]} intensity={800} color="#c9b8ff" />
						<pointLight position={[-3, 5, 4]} color="#7b5cff" intensity={30} distance={14} />
						<Avatar look={{...KLI_DEEP, face: t > 133.4 ? 'klishock' : 'kli'}} position={[0, 0, 0]} pose={{time: t, headYaw: t > 133.2 ? 0.7 : 0}} />
						<Pigeon position={[0, 6.0, 0]} t={t} flap={0} scale={0.9} />
						{cubeS > 0 ? (
							<group position={[2.4, 3.0, 0.5]} scale={cubeS}>
								<pointLight position={[0.5, 1, 2]} color="#ffd2a0" intensity={25} distance={6} />
								<DefaultCube position={[0, 0, 0]} scale={0.65} />
								{[-1, 1].map((s) => (
									<mesh key={s} position={[s * 0.3, 0.2, 0.67]}>
										<boxGeometry args={[0.14, 0.24, 0.02]} />
										<meshBasicMaterial color="#111" />
									</mesh>
								))}
							</group>
						) : null}
					</Stage>
					<Vignette amt={0.9} />
				</AbsoluteFill>
			)}
			<Grain t={t} opacity={0.06} />
			<Letterbox />
		</AbsoluteFill>
	);
};
