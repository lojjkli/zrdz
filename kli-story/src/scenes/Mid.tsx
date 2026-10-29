import React, {useMemo} from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {Avatar, KLI_DEEP, NOOB_KLI} from '../three/Avatar';
import {Cam, clamp01, ease, easeOut, lerp, lerp3, range, V3} from '../three/cam';
import {Rain, Sparkles} from '../three/Props';
import {Clouds, Env, lerpEnv, Stage} from '../three/World';
import {LightBeam, LOBBY_NIGHT} from '../three/MM2World';
import {baseplateTexture, DefaultCube, Lava, Orb, Part, ViewportGrid} from '../three/KliProps';
import {rand} from '../three/textures';
import {FPS, PARTS_DROP, talking, VOICE_DROP} from '../timeline';
import {Billboards} from '../ui/Billboards';
import {BigText, GameUI} from '../ui/MM2';
import {BlenderUI, CrackOverlay, Fade, Flash, ObbyPage, OutLine, PopWords, RobuxCounter, StudioUI} from '../ui/KliUI';
import {Shot, shotAt, withShake} from './shots';

const STUDIO_ENV: Env = {
	skyTop: '#4d8fe0',
	skyHorizon: '#cfe6ff',
	sunDir: [0.5, 0.8, 0.4],
	sunColor: '#ffffff',
	sunIntensity: 2.2,
	hemiSky: '#e0eeff',
	hemiGround: '#666',
	hemiIntensity: 1.0,
	fog: ['#cfe6ff', 150, 500],
	sunGlow: 0.5,
};

const Baseplate: React.FC<{y?: number; color?: string; k?: string}> = ({y = 0, color = '#6b6e72', k = 'grey'}) => {
	const tex = useMemo(() => baseplateTexture(k, color, k === 'grey' ? '#5c5f63' : '#2a5a2a'), [k, color]);
	return (
		<mesh position={[0, y - 0.5, 0]} receiveShadow>
			<boxGeometry args={[160, 1, 160]} />
			<meshStandardMaterial map={tex} roughness={0.85} />
		</mesh>
	);
};

// ================================================================ roblox studio fails
const COLORS = ['#e53935', '#1e88e5', '#43a047', '#fdd835', '#8e24aa', '#fb8c00', '#00acc1', '#f06292'];
const PART_SPOTS: V3[] = [
	[0, 0.5, 0],
	[4, 0.5, -2],
	[-3, 0.5, -4],
	[2, 1.5, 0],
	[6, 0.5, 3],
	[-1, 2.5, 0],
	[-5, 0.5, 1],
	[3, 0.5, -6],
];

const OUT: OutLine[] = [
	{at: 76.2, text: 'Workspace.Part is not anchored', color: '#ffb347'},
	{at: 77.4, text: 'kliScript:1: attempt to call makeGame (a nil value)'},
	{at: 78.6, text: 'Part fell out of the world', color: '#ffb347'},
	{at: 79.2, text: "Infinite yield possible on 'Skill'"},
	{at: 79.8, text: 'Script timeout: exhausted allowed execution time'},
	{at: 80.4, text: 'Part (47) fell out of the world', color: '#ffb347'},
	{at: 81.0, text: 'Roblox Studio is not responding...'},
	{at: 82.3, text: '💥 everything exploded'},
	{at: 83.8, text: 'Baseplate has left the experience.', color: '#d7d7d7'},
];

const studioPart = (i: number, t: number): {p: V3; r: V3} | null => {
	const at = PARTS_DROP(i);
	if (t < at) return null;
	const s = PART_SPOTS[i];
	const fall = range(t, at, at + 0.35);
	const wob = t > at + 0.35 ? Math.sin((t - at) * 9 + i) * 0.25 * Math.exp(-(t - at - 0.35) * 0.6) : 0;
	let p: V3 = [s[0], lerp(18, s[1], fall * fall), s[2]];
	let r: V3 = [wob + i * 0.07, i * 0.4, wob * 0.6 + (i % 3 === 0 ? 0.35 : 0)];
	if (t > 82.3) {
		const e = t - 82.3;
		const d = new Array(3).fill(0).map((_, j) => (rand(i * 3 + j) - 0.5) * 2) as V3;
		p = [p[0] + d[0] * e * 22, p[1] + 14 * e - 9 * e * e + 4, p[2] + d[2] * e * 22];
		r = [r[0] + e * 6, r[1] + e * 5, r[2]];
	}
	if (t > 83.6) p = [p[0], p[1] - (t - 83.6) * (t - 83.6) * 30, p[2]];
	return {p, r};
};

// obby
const P1: V3 = [0, 6, 0];
const P2: V3 = [0, 6, -9];
const obbyKli = (t: number): V3 => {
	if (t < 93.2) return [P1[0], P1[1], lerp(1.5, -1.6, range(t, 92.4, 93.2))];
	if (t < 94.2) {
		const k = (t - 93.2) / 1.0;
		return [0, 6 + 5 * k - 11 * k * k, lerp(-1.6, -6.2, k)];
	}
	return [0, 0, -6.2];
};

const STUDIO_SHOTS: Shot[] = [
	{from: 74, to: 86, cam: (t, k) => ({pos: lerp3([20, 13, 24], [17, 11, 21], k), target: [1, 1.5, 0], fov: 46})},
	{from: 86, to: 92.4, cam: () => ({pos: [20, 13, 24], target: [1, 1.5, 0], fov: 46})},
	{from: 92.4, to: 95.6, cam: (t, k) => ({pos: lerp3([19, 12, 0], [18, 11, -2], k), target: [0, 6, -4], fov: 50})},
	{from: 95.6, to: 100, cam: (t, k) => ({pos: lerp3([2, 10.2, 6.5], [1.6, 10, 5.6], k), target: [0, 9.4, 0], fov: 42})},
];

export const StudioScene: React.FC<{t0: number}> = ({t0}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const cam = withShake(shotAt(STUDIO_SHOTS, t).cam, t, t > 82.3 && t < 83 ? 0.15 : 0);
	const page = t >= 86 && t < 92.4;
	const obby = t >= 92.4;
	const clones = t > 79.2 ? Math.min(40, Math.floor((t - 79.2) * 22)) : 0;
	const bpY = t > 83.6 ? -(t - 83.6) * (t - 83.6) * 12 : 0;
	const kStudio: V3 = [-7, bpY, 6];
	const ok = obbyKli(t);
	const dead = obby && t >= 94.2 && t < 95.6;
	const respawned = t >= 95.6;
	return (
		<AbsoluteFill style={{background: '#000'}}>
			{!page ? (
				<Stage cam={cam} env={obby ? {...STUDIO_ENV, sunColor: '#ffd0a0', hemiGround: '#ff6a00', shadowCenter: [0, 0, -4], shadowSize: 20} : {...STUDIO_ENV, shadowCenter: [0, 0, 0], shadowSize: 24}}>
					{!obby ? (
						<>
							<Baseplate y={bpY} />
							<Avatar look={{...NOOB_KLI, face: t > 81.5 ? 'shock' : 'happy'}} position={kStudio} rotationY={0.9} pose={{time: t, armsUp: t > 82.3 ? 1 : 0, point: t > 75.6 && t < 79 ? 1 : 0}} />
							{PART_SPOTS.map((_, i) => {
								const s = studioPart(i, t);
								return s ? <Part key={i} position={s.p} rotation={s.r} size={[4, 1, 2]} color={COLORS[i % COLORS.length]} /> : null;
							})}
							{new Array(clones).fill(0).map((_, i) => {
								const e = t > 82.3 ? t - 82.3 : 0;
								const base: V3 = [(rand(i) - 0.5) * 18, 0.5 + (i % 6) * 1.0 + (t - 79.2) * 0.2, (rand(i + 7) - 0.5) * 14];
								const p: V3 = [base[0] * (1 + e * 3), base[1] + e * 12 - e * e * 9 + (t > 83.6 ? -((t - 83.6) ** 2) * 30 : 0), base[2] * (1 + e * 3)];
								return <Part key={'c' + i} position={p} rotation={[i, i * 0.7 + e * 5, 0]} size={[4, 1, 2]} color="#e53935" />;
							})}
						</>
					) : (
						<>
							<Lava t={t} y={0} />
							<Part position={[P1[0], P1[1] - 0.5, P1[2]]} size={[5, 1, 5]} color="#43a047" />
							<Part position={[P2[0], P2[1] - 0.5, P2[2]]} size={[4, 1, 4]} color="#1e88e5" />
							<Part position={[0, 5.5, -16]} size={[4, 1, 4]} color="#fdd835" />
							<pointLight position={[0, 3, -4]} color="#ff6a00" intensity={120} distance={20} decay={1.4} />
							{!dead && !respawned ? <Avatar look={{...NOOB_KLI, face: t > 93.7 ? 'scream' : 'happy'}} position={ok} rotationY={Math.PI} pose={{time: t, walk: t * 9, walkAmt: t < 93.2 ? 1 : 0, armsUp: t > 93.6 ? 1 : 0}} /> : null}
							{dead
								? new Array(6).fill(0).map((_, i) => {
										const e = t - 94.2;
										const d: V3 = [(rand(i) - 0.5) * 8, 8 + rand(i + 3) * 5, (rand(i + 5) - 0.5) * 8];
										return <Part key={i} position={[d[0] * e, Math.max(0.3, 1 + d[1] * e - 9 * e * e), -6.2 + d[2] * e]} rotation={[e * 8 + i, e * 6, 0]} size={i === 0 ? [1.4, 1.4, 1.4] : [1, 2, 1]} color={i === 0 ? '#f5cd30' : i < 3 ? '#1e6fd9' : '#4caf50'} />;
								  })
								: null}
							{respawned ? <Avatar look={{...NOOB_KLI, face: 'sad'}} position={[0, 6, 0]} rotationY={0.2} pose={{time: t, sit: 1, headPitch: 0.3}} /> : null}
						</>
					)}
				</Stage>
			) : (
				<ObbyPage t={t - 86} dislikeAt={3.6} />
			)}
			{!page && !obby ? <StudioUI t={t} out={OUT} explorer={['Baseplate', 'Part', 'Part (2)', 'kliScript', ...(clones > 0 ? ['Part (47)'] : [])]} /> : null}
			{obby ? (
				<>
					<Billboards cam={cam} t={t} items={dead ? [] : [{p: respawned ? [0, 5, 0] : ok, name: 'lojjkli', talking: talking('kli', t)}]} />
					<GameUI t={t} talking={talking('kli', t)} mode="plain" chatFrom={999} />
					<BigText t={t} from={94.3} to={95.8} text="OOF" color="#ff5b5b" top={160} size={150} />
				</>
			) : null}
			<Flash t={t} at={82.3} dur={0.3} color="#fff4c0" />
			<Fade t={t} inAt={t0} outFrom={99.4} outTo={100} />
		</AbsoluteFill>
	);
};

// ================================================================ he meets the 3D app
const FIELD: Env = {...LOBBY_NIGHT, stars: 1.2, hemiGround: '#14251a'};
const STORM: Env = {
	skyTop: '#05030c',
	skyHorizon: '#2a1840',
	sunDir: [-0.3, 0.6, 0.5],
	sunColor: '#a58cff',
	sunIntensity: 0.6,
	hemiSky: '#4a3a70',
	hemiGround: '#0b0814',
	hemiIntensity: 0.5,
	fog: ['#140c22', 30, 140],
	sunGlow: 0.3,
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
const ORB_AT: V3 = [0, 2.6, -5];
const KLI_AT: V3 = [0, 0, 0];

const orbPos = (t: number): V3 => {
	if (t < 102.6) return lerp3([10, 70, -30], ORB_AT, ease(range(t, 100.6, 102.6)) * 0.3 + range(t, 100.6, 102.6) * 0.7);
	return [ORB_AT[0], ORB_AT[1] + Math.sin(t * 2) * 0.3, ORB_AT[2]];
};

const BL_SHOTS: Shot[] = [
	{from: 100, to: 102.6, cam: (t, k) => ({pos: [3, 2.2, 9], target: lerp3([4, 22, -16], [0, 3, -4], ease(range(t, 101, 102.6))), fov: 52})},
	{from: 102.6, to: 105, cam: (t, k) => ({pos: lerp3([8, 4.5, 6], [7, 4.2, 5], k), target: [0, 2.5, -2.5], fov: 46})},
	{from: 105, to: 108.2, cam: (t, k) => ({pos: lerp3([7.4, 5.3, 6.6], [6.6, 4.8, 5.9], k), target: [0, 0.6, 0], fov: 40})},
	{from: 108.2, to: 111, cam: (t, k) => ({pos: lerp3([1.0, 3.9, -4.4], [0.8, 3.85, -3.8], k), target: [0, 3.6, 0], fov: 42})},
	{from: 111, to: VOICE_DROP, cam: (t, k) => ({pos: lerp3([1.4, 5.0, 10], [0.5, 4.8, 5.4], ease(k)), target: [0, 4.4, 0], fov: 44})},
	{from: VOICE_DROP, to: 118.4, cam: (t, k) => ({pos: lerp3([1.4, 1.2, 6.2], [1.2, 1.4, 5.4], k), target: [0, 5, 0], fov: 56})},
	{from: 118.4, to: 122.3, cam: (t, k) => {
		const a = lerp(0.6, -0.6, k);
		return {pos: [Math.sin(a) * 12, 5.5, Math.cos(a) * 12], target: [0, 3.6, 0], fov: 46};
	}},
	{from: 122.3, to: 126, cam: (t, k) => ({pos: lerp3([0.6, 4.8, 9.5], [0.4, 4.6, 8.2], k), target: [0, 4.2, 0], fov: 46})},
];

export const BlenderScene: React.FC<{t0: number}> = ({t0}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const shake = t > VOICE_DROP && t < VOICE_DROP + 0.6 ? 0.15 : t > 116.2 && t < 117.4 ? 0.1 * (1 - (t - 116.2) / 1.2) : 0;
	const cam = withShake(shotAt(BL_SHOTS, t).cam, t, shake);
	const app = t >= 105 && t < 108.2;
	const storm = t >= 111;
	const deep = t >= VOICE_DROP;
	const cubeScale = t < 107.6 ? 1 : 1 - clamp01((t - 107.6) / 0.12);
	const env = app ? VIEWPORT : storm ? lerpEnv(FIELD, STORM, range(t, 111, 113)) : FIELD;
	const kTalk = talking('kli', t);
	const kFace = deep ? 'kli' : t >= 108.2 ? 'hearts' : t >= 102.6 ? 'shock' : 'sad';
	const kSit = deep ? 0 : t >= 111 ? 1 - range(t, 111.4, 112.2) : 1;
	const bolt = t > VOICE_DROP - 0.05 && t < VOICE_DROP + 0.3;
	const wave = t > 116.2 ? (t - 116.2) * 18 : 0;
	const flex = t > 122.3 ? 1 : 0;
	return (
		<AbsoluteFill style={{background: '#000'}}>
			<Stage cam={cam} env={{...env, shadowCenter: [0, 0, -1], shadowSize: 16}}>
				{app ? (
					<>
						<ViewportGrid />
						<DefaultCube scale={cubeScale} />
					</>
				) : (
					<>
						<Baseplate color="#24452a" k="grass" />
						{storm ? <Clouds t={t} color="#2a2040" opacity={0.85} /> : null}
						{storm && !deep ? <Rain t={t} center={[0, 0, 0]} area={40} count={700} /> : null}
						{!storm ? <Orb position={orbPos(t)} t={t} /> : null}
						{t < 105 ? <LightBeam position={[ORB_AT[0], 0, ORB_AT[2]]} k={range(t, 102.4, 102.8) * (1 - range(t, 104, 105))} color="#ffcf8a" /> : null}
						<Avatar
							look={deep ? KLI_DEEP : {...NOOB_KLI, face: kFace as never}}
							position={KLI_AT}
							rotationY={!deep && t >= 102.6 && t < 111.4 ? Math.PI : 0}
							pose={{time: t, sit: kSit, headPitch: !deep && t < 102.6 ? 0.3 : !deep && t < 105 ? -0.2 : 0, flex, armsUp: !deep && t > 113 ? 0.4 : 0}}
						/>
						{deep ? <pointLight position={[0, 6, 4]} color="#b49cff" intensity={140} distance={20} decay={1.3} /> : null}
						<pointLight position={[4, 5, 7]} color="#dfe6ff" intensity={30} distance={18} decay={1.4} />
						<pointLight position={[1, 5, -4]} color="#ffd2a0" intensity={t >= 102.6 && t < 111 ? 30 : 0} distance={10} decay={1.4} />
						{bolt ? (
							<mesh position={[0, 40, 0]}>
								<boxGeometry args={[0.5, 80, 0.5]} />
								<meshBasicMaterial color="#e8e4ff" />
							</mesh>
						) : null}
						{wave > 0 && wave < 40 ? (
							<mesh position={[0, 0.1, 0]} rotation={[-Math.PI / 2, 0, 0]}>
								<ringGeometry args={[wave, wave + 0.6, 64]} />
								<meshBasicMaterial color="#c8b8ff" transparent opacity={1 - wave / 40} />
							</mesh>
						) : null}
						{t > 122.3 ? (
							<Sparkles points={new Array(16).fill(0).map((_, i) => [Math.sin(i * 2.3) * 3, 1 + (i % 5) + Math.sin(t + i) * 0.3, Math.cos(i * 2.3) * 3] as V3)} t={t} color="#ffd84d" size={0.18} />
						) : null}
					</>
				)}
			</Stage>
			{app ? (
				<>
					<BlenderUI t={t} outliner={t < 107.6 ? ['Camera', 'Light', 'Cube'] : ['Camera', 'Light']} />
					{t > 106.2 && t < 107.6 ? (
						<div style={{position: 'absolute', left: 760, top: 470, padding: '10px 18px', borderRadius: 8, background: '#1d1d1d', border: '1px solid #555', fontFamily: 'sans-serif', fontSize: 24, color: '#ddd'}}>
							Delete <span style={{color: '#888', marginLeft: 20}}>X</span>
						</div>
					) : null}
				</>
			) : (
				<>
					<Billboards cam={cam} t={t} items={[{p: KLI_AT, name: 'lojjkli', talking: kTalk, hearts: t >= 108.2 && t < 111 ? (t - 108.2) % 2.5 : undefined}]} />
					<GameUI t={t} talking={kTalk} mode="plain" chatFrom={118} />
					{t >= 108.2 && t < 111 ? <AbsoluteFill style={{background: 'radial-gradient(ellipse at center, rgba(255,120,180,0) 40%, rgba(255,80,160,0.45) 100%)'}} /> : null}
					<RobuxCounter value={0} />
				</>
			)}
			<BigText t={t} from={103.4} to={104.9} text="✨ A 3D APP ✨" color="#ffb060" top={150} />
			<CrackOverlay t={t} at={116.4} dur={2.0} x={760} y={380} seed={7} />
			<BigText t={t} from={116.4} to={118.2} text="🔊 BASS BOOSTED" color="#c8b8ff" top={140} size={100} />
			<PopWords
				t={t}
				until={125.6}
				words={[
					{at: 122.4, text: 'SMARTEST 🧠', x: 560, y: 470, rot: -5, color: '#7fd0ff'},
					{at: 123.2, text: 'STRONGEST 💪', x: 1400, y: 580, rot: 4, color: '#ffd84d'},
					{at: 124.0, text: 'COOLEST 🔥', x: 960, y: 760, rot: -2, color: '#ff8a3d'},
				]}
			/>
			<Flash t={t} at={VOICE_DROP} dur={0.8} />
			<Flash t={t} at={107.6} dur={0.15} color="#ffa21a" />
			<Fade t={t} inAt={t0} outFrom={125.5} outTo={126} />
		</AbsoluteFill>
	);
};
