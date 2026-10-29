import React, {useMemo} from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {Avatar, KLI_DEEP, Look, REQ_LOOK, rbox} from '../three/Avatar';
import {Cam, ease, easeOut, lerp, lerp3, range, V3} from '../three/cam';
import {Machine, Pet, Sparkles, Spotlight} from '../three/Props';
import {Clouds, Diamond, Env, Forest, Stage} from '../three/World';
import {LOBBY_DAY, LOBBY_NIGHT, LOBBY_SUNSET} from '../three/MM2World';
import {baseplateTexture, Pigeon} from '../three/KliProps';
import {reelTexture} from '../three/textures';
import {CURTAIN, FPS, PECK, POP, SUCK, talking, WHEEL} from '../timeline';
import {Billboards, BB} from '../ui/Billboards';
import {DOC_FONT, GAME_FONT, UI_FONT} from '../ui/HUD';
import {BigText, GameUI} from '../ui/MM2';
import {Fade, Flash} from '../ui/KliUI';
import {Grain, Letterbox, Vignette} from './Doc';
import {face, Shot, shotAt, withShake} from './shots';

const VOID: Env = {
	skyTop: '#0a0408',
	skyHorizon: '#24080e',
	sunDir: [0.3, 1, 0.4],
	sunColor: '#ffd0c8',
	sunIntensity: 0.3,
	hemiSky: '#533',
	hemiGround: '#000',
	hemiIntensity: 0.35,
	fog: ['#0c0406', 20, 70],
	sunGlow: 0,
};
const NIGHT: Env = {...LOBBY_NIGHT, hemiSky: '#8a9ad0', hemiIntensity: 1.1, sunIntensity: 1.4};
const INSIDE: Env = {skyTop: '#12002a', skyHorizon: '#3a0a4a', sunDir: [0.2, 1, 0.5], sunColor: '#ffc8f0', sunIntensity: 1.2, hemiSky: '#c070ff', hemiGround: '#200030', hemiIntensity: 0.9, fog: ['#24083a', 50, 140], sunGlow: 0};
const Y = 0.05;
const REQ = (f: Look['face']): Look => ({...REQ_LOOK, face: f});

const Grass: React.FC = () => (
	<mesh position={[0, -0.5, 0]} receiveShadow>
		<boxGeometry args={[600, 1, 600]} />
		<meshStandardMaterial map={baseplateTexture('psgrass', '#5aa83e', '#4f9a36', 140)} roughness={0.9} />
	</mesh>
);

const std = (color: string, extra: Record<string, unknown> = {}) => <meshStandardMaterial color={color} roughness={0.6} {...extra} />;

/** The hamster that runs the whole Lucky Spin. Faces +z, feet at y=0. */
const Hamster: React.FC<{position: V3; rotationY?: number; t: number; scale?: number; run?: number; shades?: boolean; tired?: boolean; jump?: number}> = ({position, rotationY = 0, t, scale = 1, run = 0, shades, tired, jump = 0}) => {
	const bob = Math.abs(Math.sin(t * 22)) * 0.12 * run + jump;
	return (
		<group position={[position[0], position[1] + bob, position[2]]} rotation={[0, rotationY, 0]} scale={scale}>
			<mesh position={[0, 0.75, 0]} geometry={rbox(1.5, 1.3, 1.7, 0.55)} castShadow>
				{std('#e8a35a')}
			</mesh>
			<mesh position={[0, 0.6, 0.62]} geometry={rbox(1.0, 0.8, 0.5, 0.3)}>
				{std('#fff3e2')}
			</mesh>
			{[-1, 1].map((s) => (
				<group key={s}>
					<mesh position={[s * 0.48, 1.45, 0.1]}>
						<sphereGeometry args={[0.24, 12, 10]} />
						{std('#d48a46')}
					</mesh>
					<mesh position={[s * 0.48, 1.45, 0.2]} scale={[1, 1, 0.4]}>
						<sphereGeometry args={[0.15, 10, 8]} />
						{std('#ffb3c1')}
					</mesh>
					<mesh position={[s * 0.3, tired ? 1.0 : 1.05, 0.86]} scale={[1, tired ? 0.35 : 1, 1]}>
						<sphereGeometry args={[0.11, 10, 8]} />
						{std('#111', {roughness: 0.2})}
					</mesh>
					<mesh position={[s * 0.5, 0.82, 0.78]} scale={[1, 0.8, 0.5]}>
						<sphereGeometry args={[0.2, 10, 8]} />
						{std('#ffcf9a')}
					</mesh>
					<mesh position={[s * 0.4, 0.12 + Math.sin(t * 22 + s) * 0.08 * run, 0.35]}>
						<boxGeometry args={[0.3, 0.24, 0.4]} />
						{std('#ffb3c1')}
					</mesh>
				</group>
			))}
			<mesh position={[0, 0.9, 0.9]}>
				<sphereGeometry args={[0.08, 8, 6]} />
				{std('#ff6b8b')}
			</mesh>
			{shades ? (
				<group position={[0, 1.07, 0.92]}>
					{[-1, 1].map((s) => (
						<mesh key={s} position={[s * 0.3, 0, 0]}>
							<boxGeometry args={[0.42, 0.24, 0.05]} />
							<meshStandardMaterial color="#111" roughness={0.1} metalness={0.6} />
						</mesh>
					))}
					<mesh>
						<boxGeometry args={[0.9, 0.05, 0.05]} />
						<meshStandardMaterial color="#111" />
					</mesh>
				</group>
			) : null}
		</group>
	);
};

/** Hamster wheel, facing +z, bottom of the ring at y = 0.4. */
const WHEEL_R = 4.2;
const Wheel: React.FC<{position: V3; angle: number}> = ({position, angle}) => (
	<group position={position}>
		<group position={[0, WHEEL_R + 0.4, 0]} rotation={[0, 0, angle]}>
			{[-1.3, 1.3].map((z) => (
				<mesh key={z} position={[0, 0, z]}>
					<torusGeometry args={[WHEEL_R, 0.16, 8, 48]} />
					<meshStandardMaterial color="#c0c6d0" metalness={0.8} roughness={0.25} />
				</mesh>
			))}
			{new Array(24).fill(0).map((_, i) => {
				const a = (i / 24) * Math.PI * 2;
				return (
					<mesh key={i} position={[Math.cos(a) * WHEEL_R, Math.sin(a) * WHEEL_R, 0]} rotation={[Math.PI / 2, 0, 0]}>
						<cylinderGeometry args={[0.06, 0.06, 2.6, 6]} />
						<meshStandardMaterial color="#9aa2ad" metalness={0.8} roughness={0.3} />
					</mesh>
				);
			})}
			{[0, 1, 2, 3].map((i) => (
				<mesh key={'s' + i} position={[0, 0, -1.3]} rotation={[0, 0, (i * Math.PI) / 4]}>
					<boxGeometry args={[WHEEL_R * 2, 0.12, 0.12]} />
					<meshStandardMaterial color="#9aa2ad" metalness={0.8} roughness={0.3} />
				</mesh>
			))}
		</group>
		<mesh position={[0, (WHEEL_R + 0.4) / 2, -1.6]}>
			<boxGeometry args={[0.3, WHEEL_R + 0.4, 0.3]} />
			<meshStandardMaterial color="#6b4a8a" />
		</mesh>
	</group>
);

const Drum: React.FC<{position: V3; t: number; speed: number}> = ({position, t, speed}) => {
	const tex = useMemo(() => reelTexture(), []);
	return (
		<mesh position={position} rotation={[t * speed, 0, Math.PI / 2]}>
			<cylinderGeometry args={[8, 8, 9, 40, 1, true]} />
			<meshStandardMaterial map={tex} emissive="#ffffff" emissiveMap={tex} emissiveIntensity={0.5} side={2} />
		</mesh>
	);
};

const Chair: React.FC<{position: V3; rotationY?: number}> = ({position, rotationY = 0}) => (
	<group position={position} rotation={[0, rotationY, 0]}>
		<mesh position={[0, 0.5, 0]} rotation={[-0.15, 0, 0]}>
			<boxGeometry args={[1.8, 0.12, 2.2]} />
			<meshStandardMaterial color="#4fd2ff" />
		</mesh>
		<mesh position={[0, 1.2, -1.0]} rotation={[-0.5, 0, 0]}>
			<boxGeometry args={[1.8, 1.6, 0.12]} />
			<meshStandardMaterial color="#4fd2ff" />
		</mesh>
		{[-0.8, 0.8].map((x) => (
			<mesh key={x} position={[x, 0.25, 0]}>
				<boxGeometry args={[0.1, 0.5, 2]} />
				<meshStandardMaterial color="#ddd" metalness={0.6} />
			</mesh>
		))}
	</group>
);

const Juice: React.FC<{position: V3}> = ({position}) => (
	<group position={position}>
		<mesh position={[0, 0.3, 0]}>
			<cylinderGeometry args={[0.2, 0.15, 0.6, 12]} />
			<meshStandardMaterial color="#ffb347" transparent opacity={0.85} />
		</mesh>
		<mesh position={[0.08, 0.7, 0]} rotation={[0, 0, -0.3]}>
			<cylinderGeometry args={[0.03, 0.03, 0.6, 6]} />
			<meshStandardMaterial color="#ff4fa0" />
		</mesh>
	</group>
);

// ================================================================ cold open
export const ColdOpen3: React.FC = () => {
	const t = useCurrentFrame() / FPS;
	const k = ease(range(t, 0, 9));
	const cam: Cam = {pos: lerp3([2, 9, 22], [5, 8, 26], k), target: lerp3([0, 7, 0], [-1, 7, 0], k), fov: 42};
	const title = range(t, 4.4, 4.9);
	const sub = range(t, 5.1, 5.7);
	const out = range(t, 8.5, 9);
	return (
		<AbsoluteFill style={{background: '#000'}}>
			<Stage cam={cam} env={VOID}>
				<Spotlight position={[0, 26, 10]} target={[0, 6, 0]} intensity={1800} color="#ffe6e0" />
				<Machine t={t} spin={[t * 3, t * 3.4, t * 3.8]} lights={0.8} />
				<Avatar look={REQ('worried')} position={[3, Y, 7]} rotationY={Math.PI} pose={{time: t}} />
			</Stage>
			<Vignette />
			<div style={{position: 'absolute', left: 120, top: 90, fontFamily: DOC_FONT, fontSize: 80, letterSpacing: 16, color: '#ffd6d0', opacity: interpolate(t, [0.4, 0.8, 3.8, 4.2], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}}>
				LAST TIME...
			</div>
			<div style={{position: 'absolute', left: 150, top: 330, opacity: title, transform: `translateX(${(1 - title) * -40}px)`}}>
				<div style={{fontFamily: DOC_FONT, fontSize: 300, color: '#fff', letterSpacing: 40, lineHeight: 1}}>REQ 3</div>
				<div style={{height: 4, width: 640 * title, background: '#ff5b5b', marginTop: 10}} />
				<div style={{fontFamily: UI_FONT, fontSize: 40, color: '#ffd6d0', marginTop: 24, letterSpacing: 10, opacity: sub, fontWeight: 600}}>INSIDE THE MACHINE</div>
			</div>
			<Grain t={t} />
			<Letterbox h={110 * (1 - out)} />
			<AbsoluteFill style={{background: '#000', opacity: Math.max(1 - t / 0.7, out)}} />
		</AbsoluteFill>
	);
};

// ================================================================ outside the machine (night, pecking, morning)
const REQ_N: V3 = [2.2, Y, 7.4];
const KLI_O: V3 = [6.5, Y, 10];
const PIG_O0: V3 = [4.6, Y + 0.6, 10.6];
const PIG_O1: V3 = [-2.4, 2.0, 3.6];
const REQ_OUT: V3 = [1.2, Y, 9.5];
const HAM_OUT: V3 = [-1.6, Y, 9.2];

const OUT_SHOTS: Shot[] = [
	{from: 9, to: 13.2, cam: (t, k) => ({pos: lerp3([20, 9, 26], [16, 8, 22], ease(k)), target: [0, 6, 2], fov: 50})},
	{from: 13.2, to: 16.2, cam: (t, k) => ({pos: lerp3([0.2, 5.2, 12.6], [0.4, 5.1, 12], k), target: [REQ_N[0], 4.3, REQ_N[2]], fov: 40})},
	{from: 16.2, to: 18.6, cam: (t, k) => ({pos: lerp3([0, 8.6, 14], [0, 8.6, 12], k), target: [0, 8.6, 2], fov: 40})},
	{from: 18.6, to: SUCK, cam: () => ({pos: [0.6, 5.2, 12.4], target: [REQ_N[0], 4.3, REQ_N[2]], fov: 40})},
	{from: SUCK, to: 24.6, cam: (t, k) => ({pos: lerp3([6, 8, 18], [3, 8.6, 13], ease(range(t, SUCK, 22))), target: [0, 8.4, 2], fov: 46})},
	// outside while REQ runs
	{from: 58.4, to: 62.4, cam: (t, k) => ({pos: lerp3([-10, 7, 20], [-9, 7, 19], k), target: [2, 5, 5], fov: 48})},
	{from: 62.4, to: 63.6, cam: () => ({pos: [5.2, 2.4, 14], target: [PIG_O0[0], 1.4, PIG_O0[2]], fov: 40})},
	{from: 63.6, to: POP, cam: (t, k) => ({pos: lerp3([-9, 4, 8], [-8.4, 4, 7.4], k), target: [-1.4, 3.2, 3], fov: 42})},
	// out
	{from: POP, to: 69.0, cam: (t, k) => ({pos: lerp3([6, 6, 22], [5, 6, 21], k), target: [0, 3, 8], fov: 50})},
	{from: 69.0, to: 71.6, cam: (t, k) => ({pos: lerp3([2.6, 3.8, 15], [2.4, 3.7, 14.5], k), target: [REQ_OUT[0], 3.2, REQ_OUT[2]], fov: 40})},
	{from: 71.6, to: 73.6, cam: (t, k) => ({pos: lerp3([-1.2, 1.6, 13.2], [-1.3, 1.5, 12.8], k), target: [HAM_OUT[0], 1.1, HAM_OUT[2]], fov: 40})},
	{from: 73.6, to: 78.2, cam: (t, k) => ({pos: lerp3([10, 9, 28], [6, 7, 24], ease(k)), target: [1, 3, 8], fov: 48})},
	{from: 78.2, to: 81, cam: (t, k) => ({pos: lerp3([2.4, 3.8, 15], [2.3, 3.7, 14.4], k), target: [REQ_OUT[0], 3.2, REQ_OUT[2]], fov: 36})},
];

export const OutsideScene: React.FC<{t0: number; mode: 'night' | 'outside' | 'out'}> = ({t0, mode}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const screaming = mode === 'outside';
	const cam = withShake(shotAt(OUT_SHOTS, t).cam, t, screaming ? 0.04 : mode === 'night' && t > SUCK && t < 21.2 ? 0.08 : 0);
	const env = mode === 'out' ? LOBBY_SUNSET : NIGHT;
	const suck = mode === 'night' ? ease(range(t, SUCK, SUCK + 1.4)) : 0;
	const reqP: V3 = lerp3(REQ_N, [0, 8.6, 2.2], suck);
	const call = mode === 'night' ? range(t, 15.8, 16.4) : 0;
	const pigK = mode === 'outside' ? ease(range(t, 63.8, 65.0)) : 0;
	const pigP: V3 = mode === 'out' ? [KLI_O[0] - 1.6, Y + 0.6, KLI_O[2]] : lerp3(PIG_O0, PIG_O1, pigK);
	const peck = mode === 'outside' && t > PECK - 0.3 && t < PECK + 0.3 ? Math.sin(((t - PECK + 0.3) / 0.6) * Math.PI) * 0.8 : 0;
	const jit: V3 = screaming ? [Math.sin(t * 50) * 0.08, 0, Math.cos(t * 43) * 0.05] : [0, 0, 0];
	const items: BB[] = [];
	if (mode === 'night' && suck < 0.6) items.push({p: reqP, name: 'REQ', talking: talking('req', t)});
	if (mode !== 'night') items.push({p: KLI_O, name: 'lojjkli', talking: talking('kli', t)}, {p: [pigP[0], pigP[1] - 0.2, pigP[2]], h: 2.2, name: 'THE PIGEON', talking: talking('pigeon', t)});
	if (mode === 'out') items.push({p: REQ_OUT, h: 3.6, name: 'REQ', talking: talking('req', t)}, {p: HAM_OUT, h: 2.0, name: 'Hamster', talking: talking('hamster', t)});
	const hamJump = mode === 'out' && t < 69 ? Math.abs(Math.sin(t * 9)) * 0.8 : 0;
	return (
		<AbsoluteFill>
			<Stage cam={cam} env={{...env, shadowCenter: [0, 0, 6], shadowSize: 40}}>
				<Grass />
				<Clouds t={t} color={mode === 'out' ? '#ffd6e6' : '#8a90a0'} opacity={0.85} />
				<Forest count={40} radius={[40, 140]} />
				<group position={jit}>
					<Machine t={t} spin={screaming ? [t * 20, t * 23, t * 26] : [0.4, 1.7, 3.1]} lights={1 + call * 1.5 + (screaming ? 0.8 : 0)} />
				</group>
				{call > 0 && suck < 1 ? <pointLight position={[0, 9, 6]} color="#ff5bd6" intensity={160 * call} distance={30} /> : null}
				{mode === 'night' ? (
					suck < 1 ? <Avatar look={REQ(t > SUCK ? 'shock' : t > 16.2 ? 'worried' : 'smile')} position={reqP} scale={1 - suck * 0.85} rotationY={t < 16.2 ? -0.4 : Math.PI + suck * 12} pose={{time: t, armsUp: t > SUCK ? 1 : 0, lean: t > 18.6 && t < SUCK ? 0.35 : 0}} /> : null
				) : (
					<>
						<Avatar look={KLI_DEEP} position={KLI_O} rotationY={mode === 'out' ? face(KLI_O, REQ_OUT) : face(KLI_O, [0, 0, 2])} pose={{time: t + 1, armsUp: screaming && t < 62 ? 1 : 0}} />
						<group position={pigP} rotation={[peck, mode === 'outside' && pigK > 0 ? 0.4 : -0.6, 0]}>
							<Pigeon position={[0, 0, 0]} t={t} flap={pigK > 0 && pigK < 1 ? 1 : 0} scale={1.4} />
						</group>
					</>
				)}
				{mode === 'out' ? (
					<>
						<Avatar look={REQ(t > 78.2 ? 'grin' : 'sick')} position={REQ_OUT} rotationY={0.2} pose={{time: t, sit: 1, headPitch: t < 73 ? 0.2 : 0}} />
						<Hamster position={HAM_OUT} rotationY={0.3} t={t} scale={1.1} jump={hamJump} />
					</>
				) : null}
				{mode === 'night' && t > SUCK && t < SUCK + 1.6 ? <Sparkles points={new Array(16).fill(0).map((_, i) => [Math.sin(i * 2.4 + t * 6) * (3 - (t - SUCK) * 1.6), 8.6 + Math.cos(i * 2.4 + t * 6) * (3 - (t - SUCK) * 1.6), 3] as V3)} t={t} color="#ff5bd6" size={0.4} /> : null}
				<Spotlight position={[0, 20, 16]} target={[0, 2, 8]} intensity={500} color="#ffd9f2" />
			</Stage>
			<Billboards cam={cam} t={t} items={items} />
			<GameUI t={t} talking={talking('req', t)} mode="plain" chatFrom={58.4} />
			{mode === 'outside' ? <BigText t={t} from={58.6} to={62.2} text="AAAAAAAAAAA" color="#ff4d4d" top={430} size={100} /> : null}
			{mode === 'outside' ? <BigText t={t} from={PECK} to={PECK + 0.6} text="*peck*" color="#ffd28a" top={160} size={90} /> : null}
			{mode === 'out' ? <BigText t={t} from={67.0} to={68.8} text="🐹 FREEDOM" color="#ffb36b" top={150} size={110} /> : null}
			{mode === 'out' ? <BigText t={t} from={78.3} to={80.6} text="...probably 💀" color="#fff" top={150} size={90} /> : null}
			{mode === 'night' ? <Flash t={t} at={21.0} dur={0.6} color="#ff5bd6" /> : null}
			{mode === 'out' ? <Flash t={t} at={POP} dur={0.6} /> : null}
			<Fade t={t} inAt={t0} inDur={mode === 'night' ? 0.5 : 0.05} outFrom={mode === 'night' ? 24.0 : mode === 'out' ? 80.5 : 999} outTo={mode === 'night' ? 24.6 : mode === 'out' ? 81 : 1000} />
		</AbsoluteFill>
	);
};

// ================================================================ inside the machine
const REQ_I: V3 = [0, Y, 8];
const WHEEL_P: V3 = [0, 0, -10];
const HAM_W: V3 = [0, 0.4, -10];
const HAM_CHAIR: V3 = [6, 0, -7];
const curtainOpen = (t: number) => ease(range(t, CURTAIN, CURTAIN + 1.2));

const INSIDE_SHOTS: Shot[] = [
	{from: 24.6, to: 27.0, cam: (t, k) => ({pos: lerp3([2, 5, 16], [2.4, 5, 15], k), target: [0, 4, 8], fov: 44})},
	{from: 27.0, to: 30.2, cam: (t, k) => ({pos: lerp3([14, 14, 30], [10, 12, 26], ease(k)), target: [0, 10, -20], fov: 55})},
	{from: 30.2, to: 34.8, cam: (t, k) => ({pos: lerp3([0, 2, 16], [0, 1.6, 14.5], k), target: [0, 14, -20], fov: 58})},
	{from: 34.8, to: 36.6, cam: () => ({pos: [1.4, 5.2, 13.2], target: [0, 4.3, 8], fov: 40})},
	{from: 36.6, to: 40.4, cam: (t, k) => ({pos: lerp3([2, 5, 16], [1.5, 4.6, 12], ease(k)), target: [0, 4, -6], fov: 46})},
	{from: 40.4, to: 44.4, cam: (t, k) => ({pos: lerp3([1.4, 2.4, -1.5], [0.9, 2.0, -3.6], ease(k)), target: [0, 1.2, -10], fov: 44})},
	{from: 44.4, to: 46.2, cam: () => ({pos: [0.6, 1.6, -5.4], target: [0, 1.2, -10], fov: 38})},
	{from: 46.2, to: 48.2, cam: () => ({pos: [1.4, 4.7, -7.6], target: [0, 4.4, -4.5], fov: 42})},
	{from: 48.2, to: 50.6, cam: (t, k) => ({pos: lerp3([0.6, 1.6, -5.4], [0.5, 1.5, -5.8], k), target: [0, 1.2, -10], fov: 38})},
	// REQ runs
	{from: 50.6, to: WHEEL - 0.6, cam: () => ({pos: [1.4, 4.7, -7.6], target: [0, 4.4, -4.5], fov: 42})},
	{from: WHEEL - 0.6, to: WHEEL, cam: () => ({pos: [5, 5, 0], target: [0, 4, -10], fov: 52})},
	{from: WHEEL, to: 56.8, cam: (t, k) => ({pos: lerp3([5, 5, 0], [4.4, 5, -1], k), target: [1, 4, -10], fov: 52})},
	{from: 56.8, to: 58.4, cam: () => ({pos: [6, 5.2, -3.6], target: [0, 4.4, -10], fov: 42})},
];

export const InsideScene: React.FC<{t0: number; mode: 'inside' | 'run'}> = ({t0, mode}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const cam = withShake(shotAt(INSIDE_SHOTS, t).cam, t, (mode === 'inside' && t > 42.3 && t < 42.8) || (mode === 'run' && t > 56.8) ? 0.06 : 0);
	const land = mode === 'inside' ? easeOut(range(t, 24.6, 24.9)) : 1;
	const running = mode === 'run' && t > WHEEL;
	const reqP: V3 = running ? [0, 0.4, -10] : mode === 'run' ? lerp3([0, Y, -4], [0, 0.4, -10], ease(range(t, WHEEL - 0.6, WHEEL))) : t > 44.0 ? [0, Y, -4.5] : [REQ_I[0], REQ_I[1] + (1 - land) * 12, REQ_I[2]];
	const walkUp = mode === 'inside' && t > 43.2 && t < 44.0;
	const reqPos: V3 = walkUp ? lerp3(REQ_I, [0, Y, -4.5], range(t, 43.2, 44.0)) : reqP;
	const runSpeed = running ? 4 + (t - WHEEL) * 3 : 0;
	const wheelAng = mode === 'inside' ? -t * 3 : running ? -(t - WHEEL) * (4 + (t - WHEEL) * 1.5) : 0;
	const open = mode === 'inside' ? curtainOpen(t) : 1;
	const hamOnWheel = mode === 'inside';
	const items: BB[] = [{p: reqPos, name: 'REQ', talking: talking('req', t)}];
	if (open > 0.5) items.push({p: hamOnWheel ? HAM_W : HAM_CHAIR, h: 2.2, name: 'Hamster', talking: talking('hamster', t)});
	const rf: Look['face'] = running ? (t > 56.8 ? 'scream' : 'sick') : t > 40.4 ? 'sad' : t > 34.8 ? 'worried' : 'shock';
	return (
		<AbsoluteFill>
			<Stage cam={cam} env={{...INSIDE, shadowCenter: [0, 0, 0], shadowSize: 40}}>
				<mesh position={[0, -0.5, 0]} receiveShadow>
					<boxGeometry args={[120, 1, 120]} />
					<meshStandardMaterial color="#2a0a3a" roughness={0.3} metalness={0.3} />
				</mesh>
				{[-14, 0, 14].map((x, i) => (
					<Drum key={x} position={[x, 16, -34]} t={t} speed={mode === 'run' ? 2 + (t - 50.6) * 1.5 : 0.4 + i * 0.1} />
				))}
				{[0, 1, 2, 3, 4, 5].map((i) => (
					<Diamond key={i} position={[-20 + i * 8, 8 + Math.sin(t + i) * 2, -16 - (i % 2) * 6]} t={t + i} scale={1.4} />
				))}
				<Pet kind="cat" position={[-16, 6 + Math.sin(t) * 1.5, -12]} rotationY={0.5} t={t} scale={2.2} />
				<Pet kind="dog" position={[16, 6 + Math.cos(t) * 1.5, -12]} rotationY={-0.5} t={t} scale={2.2} />
				{/* the curtain */}
				{[-1, 1].map((s) => (
					<mesh key={s} position={[s * (3.2 + open * 6), 5, -5.5]} castShadow>
						<boxGeometry args={[6.4, 10, 0.4]} />
						<meshStandardMaterial color="#b0123e" roughness={0.7} />
					</mesh>
				))}
				<mesh position={[0, 10.4, -5.5]}>
					<boxGeometry args={[14, 0.8, 0.6]} />
					<meshStandardMaterial color="#ffc93c" metalness={0.8} roughness={0.25} />
				</mesh>
				<Wheel position={WHEEL_P} angle={wheelAng} />
				{hamOnWheel ? (
					<Hamster position={HAM_W} t={t} scale={1.0} run={1} tired={t > 44} />
				) : (
					<>
						<Chair position={HAM_CHAIR} rotationY={-0.4} />
						<Hamster position={[HAM_CHAIR[0], 0.6, HAM_CHAIR[2] - 0.3]} rotationY={-0.4} t={t} scale={0.9} shades />
						<Juice position={[HAM_CHAIR[0] + 1.3, 0, HAM_CHAIR[2] + 0.4]} />
					</>
				)}
				{/* the microphone the "voice" uses */}
				<group position={[-2.6, 0, -8.5]}>
					<mesh position={[0, 0.8, 0]}>
						<cylinderGeometry args={[0.05, 0.3, 1.6, 8]} />
						<meshStandardMaterial color="#333" metalness={0.6} />
					</mesh>
					<mesh position={[0, 1.7, 0]}>
						<sphereGeometry args={[0.22, 12, 10]} />
						<meshStandardMaterial color="#888" metalness={0.8} roughness={0.3} />
					</mesh>
				</group>
				<Avatar look={REQ(rf)} position={reqPos} rotationY={walkUp || (t > 44 && mode === 'inside') || (mode === 'run' && !running) ? Math.PI : running ? Math.PI / 2 : 0} pose={{time: t, walk: running ? t * runSpeed * 2 : t * 10, walkAmt: running || walkUp ? 1 : 0, armsUp: t < 27 || (running && t > 56.8) ? 1 : 0, headPitch: t > 30.2 && t < 34.8 ? -0.4 : 0}} />
				<pointLight position={[0, 9, -2]} color="#ff9ad5" intensity={60} distance={30} />
				<pointLight position={[0, 6, -8]} color="#fff2c4" intensity={40 * open} distance={14} />
			</Stage>
			<Billboards cam={cam} t={t} items={items} />
			<GameUI t={t} talking={talking('req', t)} mode="plain" hideChat />
			{mode === 'inside' ? (
				<>
					<BigText t={t} from={30.4} to={34.6} text="SPINS: 4,000" color="#ff5bd6" top={150} size={100} />
					<BigText t={t} from={42.4} to={44.2} text="🐹" color="#fff" top={150} size={150} />
				</>
			) : (
				<BigText t={t} from={56.8} to={58.4} text="AAAAAAAAAAA" color="#ff4d4d" top={150} size={110} />
			)}
			<Fade t={t} inAt={t0} inDur={0.05} />
		</AbsoluteFill>
	);
};

// ================================================================ end card + best day ever
export const EndCard3: React.FC<{t0: number}> = ({t0}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const lt = t - t0;
	const fadeOut = range(t, 86.4, 87);
	const soon = range(t, 82.7, 83.3);
	const post = t > 87.2;
	const cam: Cam = {pos: lerp3([2.6, 2.4, 7.5], [2.0, 2.0, 6.0], ease(range(t, 87.2, 93))), target: [0, 1.0, 0], fov: 42};
	return (
		<AbsoluteFill style={{background: '#000'}}>
			{!post ? (
				<AbsoluteFill style={{opacity: 1 - fadeOut}}>
					<div style={{position: 'absolute', left: 0, right: 0, top: 250, display: 'flex', justifyContent: 'center', gap: 40}}>
						{['R', 'E', 'Q', '3'].map((l, i) => {
							const k = ease(range(lt, 0.2 + i * 0.25, 0.6 + i * 0.25));
							return (
								<div key={l} style={{fontFamily: DOC_FONT, fontSize: 320, lineHeight: 1, color: i === 3 ? '#ff5b5b' : '#fff', opacity: k, transform: `translateY(${(1 - k) * -80}px) scale(${1.3 - 0.3 * k})`, marginLeft: i === 3 ? 50 : 0}}>
									{l}
								</div>
							);
						})}
					</div>
					<div style={{position: 'absolute', left: '50%', top: 590, width: 620 * ease(range(lt, 1.2, 1.8)), height: 5, background: '#ff5b5b', transform: 'translateX(-50%)'}} />
					<div style={{position: 'absolute', left: 0, right: 0, top: 700, textAlign: 'center', fontFamily: DOC_FONT, fontSize: 110, letterSpacing: 18, color: '#ffd6d0', opacity: soon}}>THE END</div>
				</AbsoluteFill>
			) : (
				<AbsoluteFill style={{opacity: interpolate(t, [87.2, 87.5, 92.5, 93], [0, 1, 1, 0], {extrapolateRight: 'clamp'})}}>
					<Stage cam={cam} env={{...LOBBY_DAY, shadowCenter: [0, 0, 0], shadowSize: 20}}>
						<Grass />
						<Clouds t={t} />
						<Chair position={[0, 0, 0]} rotationY={0.3} />
						<Hamster position={[0, 0.6, -0.3]} rotationY={0.3} t={t} scale={0.9} shades />
						<Juice position={[1.4, 0, 0.6]} />
					</Stage>
					<Billboards cam={cam} t={t} items={[{p: [0, 0.6, -0.3], h: 2.0, name: 'Hamster', talking: talking('hamster', t)}]} />
					<div style={{position: 'absolute', left: 0, right: 0, top: 140, textAlign: 'center', fontFamily: GAME_FONT, fontWeight: 700, fontSize: 70, color: '#fff', WebkitTextStroke: '10px #121212', paintOrder: 'stroke fill', opacity: range(t, 88.0, 88.4)}}>
						DAY 1 OF RETIREMENT 🌴
					</div>
				</AbsoluteFill>
			)}
			<Grain t={t} opacity={0.06} />
			<Letterbox />
		</AbsoluteFill>
	);
};
