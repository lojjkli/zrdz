import React, {useMemo} from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {ADE_LOOK, Avatar, BOOMP_LOOK, kidLook, KLI_LOOK, LIA_LOOK, Look, MIKEY_LOOK, REQ_LOOK} from '../three/Avatar';
import {Cam, ease, easeOut, lerp, lerp3, range, V3} from '../three/cam';
import {Pet, Sparkles, Spotlight} from '../three/Props';
import {Clouds, Env, lerpEnv, Stage} from '../three/World';
import {DutchFlag, GasCloud, LOBBY_DAY, LOBBY_NIGHT, LOBBY_SUNSET, Tulips, Windmill} from '../three/MM2World';
import {baseplateTexture, Pigeon, TalkingDonut} from '../three/KliProps';
import {rand, signTexture} from '../three/textures';
import {BLOW, BOUNCE, FART, FPS, RISE, talking} from '../timeline';
import {Billboards, BB} from '../ui/Billboards';
import {DOC_FONT, UI_FONT} from '../ui/HUD';
import {BigText, GameUI} from '../ui/MM2';
import {Fade, Flash} from '../ui/KliUI';
import {Grain, Letterbox, Vignette} from './Doc';
import {face, Shot, shotAt, withShake} from './shots';

const VOID: Env = {
	skyTop: '#0a0412',
	skyHorizon: '#1a0a24',
	sunDir: [0.3, 1, 0.4],
	sunColor: '#ffc8e8',
	sunIntensity: 0.3,
	hemiSky: '#534',
	hemiGround: '#000',
	hemiIntensity: 0.35,
	fog: ['#0c0612', 20, 70],
	sunGlow: 0,
};
const STORM: Env = {...LOBBY_DAY, skyTop: '#2a2f3d', skyHorizon: '#5a5f6e', sunColor: '#c8d0e0', sunIntensity: 1.2, hemiIntensity: 0.8, fog: ['#4a4f5e', 90, 320], sunGlow: 0};
const NIGHT: Env = {...LOBBY_NIGHT, hemiSky: '#8a9ad0', hemiIntensity: 1.3, sunIntensity: 1.7};
const Y = 0.4;

const KID67: Look = {...kidLook(67), hat: 'cap', hatColor: '#e53935', hair: undefined, face: 'grin'};
const LIA = (f: Look['face']): Look => ({...LIA_LOOK, face: f});

// cast spots, shared by every scene at the house
const LIA_P: V3 = [-3, Y, -3];
const BOOMP_P: V3 = [0, Y, -3];
const PIG_P: V3 = [3, Y, -3];
const MIKEY_P: V3 = [-6.5, Y, -1];
const ADE_P: V3 = [6.5, Y, -1];
const REQ_H: V3 = [10, Y, 1];
const KID67_P: V3 = [4, Y, 9];

// ================================================================ world
const Grass: React.FC = () => (
	<mesh position={[0, -0.1, 0]} receiveShadow>
		<boxGeometry args={[500, 1, 500]} />
		<meshStandardMaterial map={baseplateTexture('richgrass', '#4f9a3a', '#468a33', 120)} roughness={0.9} />
	</mesh>
);

const House: React.FC = () => (
	<group position={[0, 0, -12]}>
		<mesh position={[0, 5, 0]} castShadow receiveShadow>
			<boxGeometry args={[18, 10, 8]} />
			<meshStandardMaterial color="#a5452f" roughness={0.85} />
		</mesh>
		<mesh position={[0, 13, 0]} rotation={[0, Math.PI / 4, 0]} scale={[1.45, 1, 0.75]} castShadow>
			<coneGeometry args={[9, 6, 4]} />
			<meshStandardMaterial color="#3a2a22" roughness={0.9} />
		</mesh>
		{[-6, -2.2, 2.2, 6].map((x) => (
			<mesh key={x} position={[x, 7, 4.02]}>
				<planeGeometry args={[2, 2.2]} />
				<meshStandardMaterial color="#fff2b0" emissive="#ffd86b" emissiveIntensity={0.3} />
			</mesh>
		))}
		<mesh position={[0, 1.8, 4.02]}>
			<planeGeometry args={[2.4, 3.6]} />
			<meshStandardMaterial color="#2f5d3a" />
		</mesh>
	</group>
);

const Field: React.FC<{t: number}> = ({t}) => (
	<>
		<Grass />
		<House />
		<Windmill position={[-30, 0, -40]} t={t + 2} s={1.1} rotationY={0.3} />
		<Tulips center={[-19, 0, 2]} w={12} d={8} rows={6} />
		<Tulips center={[24, 0, 8]} w={18} d={14} rows={8} />
		<DutchFlag position={[-10, 0, -6]} t={t} />
	</>
);

/** The windmill, but alive. Front (+z) is its face. */
const GiantMill: React.FC<{p: V3; s: number; yaw: number; spin: number; fall?: number; tilt?: number; eyes?: number; mood?: 'angry' | 'love' | 'happy'}> = ({p, s, yaw, spin, fall = 0, tilt = 0, eyes = 1, mood = 'angry'}) => {
	const eyeCol = mood === 'angry' ? '#ff2a1a' : '#ffffff';
	return (
		<group position={p} rotation={[0, yaw, 0]}>
			<group rotation={[tilt, 0, -fall * Math.PI * 0.5]} scale={s}>
				<Windmill position={[0, 0, 0]} t={spin / 1.4} s={1} />
				{eyes > 0
					? [-1, 1].map((k) => (
							<group key={k} position={[k * 1.25, 6.6, 3.8]} rotation={[0, 0, mood === 'angry' ? k * 0.35 : 0]}>
								<mesh scale={[1, mood === 'happy' ? 0.35 : 1, 1]}>
									<boxGeometry args={[1.3, mood === 'angry' ? 0.6 : 1.1, 0.2]} />
									<meshStandardMaterial color={eyeCol} emissive={eyeCol} emissiveIntensity={1.6 * eyes} />
								</mesh>
								{mood === 'love' ? (
									<mesh position={[0, 0, 0.12]}>
										<boxGeometry args={[0.6, 0.6, 0.05]} />
										<meshBasicMaterial color="#ff4f9a" />
									</mesh>
								) : null}
							</group>
					  ))
					: null}
				{mood !== 'angry' && eyes > 0
					? [-1, 1].map((k) => (
							<mesh key={'b' + k} position={[k * 2.3, 5.4, 3.75]}>
								<circleGeometry args={[0.55, 16]} />
								<meshBasicMaterial color="#ff8fb8" transparent opacity={0.85} />
							</mesh>
					  ))
					: null}
			</group>
		</group>
	);
};

// kids: 66 in a grid on the left lawn
const KIDS: {p: V3; i: number}[] = (() => {
	const out: {p: V3; i: number}[] = [];
	for (let r = 0; r < 6; r++)
		for (let c = 0; c < 11; c++) {
			const i = r * 11 + c;
			out.push({p: [-18 + c * 1.9 + (rand(i) - 0.5) * 0.7, Y, 6 + r * 2.0 + (rand(i + 50) - 0.5) * 0.6], i});
		}
	return out;
})();

const Kids: React.FC<{t: number; yaw: (p: V3, n: number) => number; pose: (n: number) => Record<string, number>}> = ({t, yaw, pose}) => {
	const looks = useMemo(() => KIDS.map((k) => kidLook(k.i)), []);
	return (
		<>
			{KIDS.map((k, n) => (
				<Avatar key={k.i} look={looks[n]} position={k.p} scale={0.45} rotationY={yaw(k.p, n)} pose={{time: t + n * 0.37, ...pose(n)}} />
			))}
		</>
	);
};

const Bouquet: React.FC<{p: V3}> = ({p}) => (
	<group position={p}>
		{['#e5383b', '#ffba08', '#ff70a6', '#ffffff', '#9d4edd'].map((c, i) => (
			<group key={i} position={[(i - 2) * 0.22, 0, Math.sin(i * 2) * 0.15]} rotation={[0, 0, (i - 2) * 0.18]}>
				<mesh position={[0, 0.5, 0]}>
					<boxGeometry args={[0.08, 1, 0.08]} />
					<meshStandardMaterial color="#2e7d32" />
				</mesh>
				<mesh position={[0, 1.1, 0]}>
					<cylinderGeometry args={[0.24, 0.13, 0.42, 6]} />
					<meshStandardMaterial color={c} />
				</mesh>
			</group>
		))}
	</group>
);

// ---------------------------------------------------------------- windmill + REQ paths
const MILL0: V3 = [18, 0, -24];
const BIG = 2.2;
const C: V3 = [24, 0, 6];
const RAD = 11;
const CHASE0 = 37.5;
const reqAng = (t: number) => (t - CHASE0) * 0.9;
const reqChase = (t: number): V3 => {
	const a = reqAng(t);
	return [C[0] + Math.cos(a) * RAD, Y, C[2] + Math.sin(a) * RAD];
};
const reqYawChase = (t: number) => {
	const a = reqAng(t);
	return Math.atan2(-Math.sin(a), Math.cos(a));
};
const hop = (t: number) => Math.abs(Math.sin(((t - 38.0) * Math.PI) / 0.9));
const millChase = (t: number): V3 => {
	const a = reqAng(t) - 1.25;
	return [C[0] + Math.cos(a) * RAD * 0.75, hop(t) * 3, C[2] + Math.sin(a) * RAD * 0.75];
};
const R_S: V3 = [20, Y, 16];
const W_S: V3 = [26, 0, -4];
const DIR: V3 = (() => {
	const dx = R_S[0] - W_S[0];
	const dz = R_S[2] - W_S[2];
	const l = Math.hypot(dx, dz);
	return [dx / l, 0, dz / l];
})();
const MILL_YAW_S = face(W_S, R_S);
const millFaceCam = (d = 24): Cam => ({pos: [W_S[0] + DIR[0] * d + 2, 13, W_S[2] + DIR[2] * d], target: [W_S[0], 13.5, W_S[2]], fov: 40});
const reqFront = (d = 6): Cam => ({pos: [R_S[0] - DIR[0] * d + 1, 5, R_S[2] - DIR[2] * d], target: [R_S[0], 4.2, R_S[2]], fov: 40});

/** point on blade 0 tip, world space (blades at local [0,13,3.4], spin about z) */
const bladeTip = (p: V3, s: number, yaw: number, ang: number, r = 7): V3 => {
	const lx = -r * Math.sin(ang);
	const ly = 13 + r * Math.cos(ang);
	const lz = 4.0;
	return [p[0] + s * (lx * Math.cos(yaw) + lz * Math.sin(yaw)), p[1] + s * ly, p[2] + s * (-lx * Math.sin(yaw) + lz * Math.cos(yaw))];
};

const Family: React.FC<{t: number; f?: Look['face']; pose?: (i: number) => Record<string, number>; yaw?: number}> = ({t, f = 'lia', pose = () => ({}), yaw = 0}) => (
	<>
		<Avatar look={LIA(f)} position={LIA_P} rotationY={yaw} pose={{time: t, ...pose(0)}} />
		<Avatar look={BOOMP_LOOK} position={BOOMP_P} rotationY={yaw} pose={{time: t + 1, ...pose(1)}} />
		<Avatar look={MIKEY_LOOK} position={MIKEY_P} rotationY={yaw + 0.3} pose={{time: t + 2, ...pose(2)}} />
		<Avatar look={ADE_LOOK} position={ADE_P} rotationY={yaw - 0.3} pose={{time: t + 3, ...pose(3)}} />
		<Avatar look={KID67} position={KID67_P} scale={0.45} rotationY={yaw} pose={{time: t + 4, ...pose(4)}} />
		<Pet kind="dragon" gold position={[KID67_P[0] + 1.6, Y - 0.2, KID67_P[2]]} rotationY={yaw} t={t} scale={0.7} />
	</>
);

// ================================================================ cold open
export const ColdOpen3: React.FC = () => {
	const t = useCurrentFrame() / FPS;
	const k = ease(range(t, 0, 9.5));
	const cam: Cam = {pos: lerp3([6, 9, 26], [10, 7, 30], k), target: lerp3([0, 9, 0], [0, 10, 0], k), fov: 42};
	const title = range(t, 4.6, 5.1);
	const sub = range(t, 5.3, 5.9);
	const out = range(t, 9.0, 9.5);
	const eyes = t > 2.2 ? 1 : 0;
	return (
		<AbsoluteFill style={{background: '#000'}}>
			<Stage cam={cam} env={VOID}>
				<mesh position={[0, -0.25, 0]} receiveShadow>
					<cylinderGeometry args={[9, 9.3, 0.5, 48]} />
					<meshStandardMaterial color="#2a1f2c" roughness={0.3} metalness={0.4} />
				</mesh>
				<Spotlight position={[0, 34, 10]} target={[0, 8, 0]} intensity={2600} color="#ffd8d0" />
				<GiantMill p={[0, 0, 0]} s={1} yaw={0.15} spin={t * 0.6} eyes={eyes} />
				<pointLight position={[0, 10, 8]} color="#ff2a1a" intensity={60 * eyes} distance={14} />
			</Stage>
			<Vignette />
			<div style={{position: 'absolute', left: 120, top: 90, fontFamily: DOC_FONT, fontSize: 80, letterSpacing: 16, color: '#ffd6ec', opacity: interpolate(t, [0.4, 0.8, 4.0, 4.4], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}}>
				LAST TIME...
			</div>
			<div style={{position: 'absolute', left: 150, top: 330, opacity: title, transform: `translateX(${(1 - title) * -40}px)`}}>
				<div style={{fontFamily: DOC_FONT, fontSize: 300, color: '#fff', letterSpacing: 40, lineHeight: 1}}>LIA 3</div>
				<div style={{height: 4, width: 640 * title, background: '#ff6b4a', marginTop: 10}} />
				<div style={{fontFamily: UI_FONT, fontSize: 40, color: '#ffd6cc', marginTop: 24, letterSpacing: 10, opacity: sub, fontWeight: 600}}>THE WINDMILL STRIKES BACK</div>
			</div>
			<Grain t={t} />
			<Letterbox h={110 * (1 - out)} />
			<AbsoluteFill style={{background: '#000', opacity: Math.max(1 - t / 0.7, out)}} />
		</AbsoluteFill>
	);
};

// ================================================================ morning + the windmill rises (one continuous place)
const HOME_SHOTS: Shot[] = [
	{from: 9.5, to: 13.6, cam: (t, k) => ({pos: lerp3([30, 20, 44], [24, 15, 36], ease(k)), target: [0, 3, 0], fov: 50})},
	{from: 13.6, to: 16.2, cam: (t, k) => ({pos: lerp3([1.8, 5.4, 6.5], [1.8, 5.2, 5.8], k), target: [1.5, 3.4, -3], fov: 44})},
	{from: 16.2, to: 18.2, cam: (t, k) => ({pos: lerp3([3.5, 2.0, 0.6], [3.4, 1.9, 0.2], k), target: [3, 1.3, -3], fov: 40})},
	{from: 18.2, to: 20.4, cam: (t, k) => ({pos: lerp3([-2.2, 5, 1.6], [-2.4, 4.9, 1.0], k), target: [-3, 4.3, -3], fov: 40})},
	{from: 20.4, to: 23.4, cam: (t, k) => ({pos: [12, 9, 24], target: [8, 4, -8], fov: 52})},
	// rise
	{from: 23.4, to: 27.4, cam: (t, k) => ({pos: lerp3([10, 6, 16], [9, 5, 18], k), target: lerp3([18, 4, -24], [18, 20, -24], ease(range(t, RISE, 27))), fov: 58})},
	{from: 27.4, to: 29.8, cam: (t, k) => ({pos: lerp3([11.6, 12.5, -2], [11.9, 13, -3], k), target: [18, 13.5, -24], fov: 42})},
	{from: 29.8, to: 31.2, cam: () => ({pos: [11.5, 5, 6.5], target: [10, 4.3, 1], fov: 40})},
	{from: 31.2, to: 34.0, cam: (t, k) => ({pos: [15.5, 2.0, 4], target: [18, 14, -24], fov: 58})},
	{from: 34.0, to: 36.0, cam: (t, k) => ({pos: lerp3([-8, 6, 28], [-8, 6, 27], k), target: [-8, 2, 12], fov: 50})},
	{from: 36.0, to: 37.5, cam: () => ({pos: [-2.4, 5, 1.6], target: [-3, 4.3, -3], fov: 40})},
];

export const HomeScene: React.FC<{t0: number; mode: 'home' | 'rise'}> = ({t0, mode}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const quake = (t > 20.4 && t < 23.4) || (t > RISE && t < 27.0) ? 0.08 : t > 31.3 && t < 31.6 ? 0.15 : t > 32.1 && t < 32.5 ? 0.2 : 0;
	const cam = withShake(shotAt(HOME_SHOTS, t).cam, t, quake);
	const env = lerpEnv(LOBBY_DAY, STORM, range(t, 20.4, 27));
	const rk = ease(range(t, RISE, 27.0));
	const millYaw = lerp(-0.5, face(MILL0, REQ_H), rk);
	const eyes = range(t, 27.0, 27.3);
	const six = t > 34 && t < 36;
	const scared = t > 27.2;
	const lf: Look['face'] = t > 36 ? 'liashock' : t > 18.2 && t < 20.4 ? 'liasad' : scared ? 'liashock' : 'lia';
	const items: BB[] = [
		{p: LIA_P, name: 'Lia', talking: talking('lia', t)},
		{p: BOOMP_P, name: 'BoompjeJunior', talking: talking('boomp', t)},
		{p: [PIG_P[0], Y, PIG_P[2]], h: 2.6, name: 'Kid #68', talking: talking('pigeon', t)},
		{p: REQ_H, name: 'REQ', talking: talking('req', t)},
	];
	return (
		<AbsoluteFill>
			<Stage cam={cam} env={{...env, shadowCenter: [4, 0, -4], shadowSize: 50}}>
				<Field t={t} />
				{env !== LOBBY_DAY ? <Clouds t={t} color={t > 22 ? '#8a90a0' : '#ffffff'} opacity={0.9} /> : null}
				<GiantMill p={MILL0} s={lerp(1.3, BIG, rk)} yaw={millYaw} spin={t * 1.4} fall={1 - rk} eyes={eyes} />
				{eyes > 0 ? <pointLight position={[MILL0[0], 22, MILL0[2] + 10]} color="#ff2a1a" intensity={200} distance={40} /> : null}
				<Family t={t} f={lf} yaw={scared ? 0.6 : 0} pose={(i) => ({armsUp: t > 27.2 && t < 34 ? 1 : 0, wave: i === 1 && t > 13.6 && t < 16.2 ? 1 : 0, sixSeven: six && i === 4 ? 1 : 0})} />
				<Pigeon position={[PIG_P[0], Y + 0.5, PIG_P[2]]} t={t} flap={t > 16.2 && t < 17.0 ? 1 : 0} scale={1.6} />
				<Avatar look={{...REQ_LOOK, face: t > 29.6 ? 'shock' : 'smile'}} position={REQ_H} rotationY={t > 27.4 ? face(REQ_H, MILL0) * (t > 29.8 && t < 31.2 ? 0 : 1) : 0} pose={{time: t + 5, point: t > 29.8 && t < 31.2 ? 1 : 0, armsUp: t > 31.2 ? 1 : 0}} />
				<Kids t={t} yaw={(p, i) => (scared ? face(p, MILL0) : Math.sin(i * 1.7) * 0.4)} pose={(i) => ({sixSeven: six ? 1 : 0, jump: six ? Math.abs(Math.sin(t * 7 + i)) * 1.4 : 0, armsUp: scared && !six ? 1 : 0})} />
				{t > RISE && t < 28 ? <Sparkles points={new Array(16).fill(0).map((_, i) => [MILL0[0] - 8 + i * 1.1, 1 + (i % 4) * 1.2 + (t - RISE) * 1.2, MILL0[2] + Math.sin(i) * 4] as V3)} t={t} color="#9a8a70" size={1.0} /> : null}
			</Stage>
			<Billboards cam={cam} t={t} items={items} />
			<GameUI t={t} talking={talking('lia', t)} mode="plain" chatFrom={t0} />
			<BigText t={t} from={16.3} to={18.1} text="KIDS: 68 🕊️" color="#ffffff" top={150} size={100} />
			<BigText t={t} from={34.1} to={35.9} text="(not helping)" color="#ffd23f" top={150} size={80} />
			<Flash t={t} at={27.0} dur={0.3} color="#ff3a1a" />
			<Fade t={t} inAt={t0} inDur={mode === 'rise' ? 0.01 : 0.5} />
		</AbsoluteFill>
	);
};

// ================================================================ chase
const KLI_P: V3 = [3.5, Y, 6];
const DONUT0: V3 = [6.5, Y, 7.5];
const DONUT_REST: V3 = [10, Y, 13];
const KLI_IN: [number, number] = [49.4, 51.0];
const kliPos = (t: number): V3 => (t < KLI_IN[1] ? lerp3([-30, 30, 40], KLI_P, easeOut(range(t, KLI_IN[0], KLI_IN[1]))) : KLI_P);
const donutPos = (t: number): {p: V3; lying: number; spin: number} => {
	if (t < 53.8) return {p: DONUT0, lying: 0, spin: 0};
	const hit = millChase(BOUNCE);
	const toward: V3 = lerp3(DONUT0, hit, 0.8);
	if (t < BOUNCE) {
		const k = range(t, 53.8, BOUNCE);
		return {p: lerp3(DONUT0, toward, k), lying: 0, spin: k * 8};
	}
	const k = range(t, BOUNCE, BOUNCE + 0.9);
	const p = lerp3(toward, DONUT_REST, k);
	return {p: [p[0], p[1] + Math.sin(k * Math.PI) * 6, p[2]], lying: k, spin: 8 + k * 6};
};

const CHASE_SHOTS: Shot[] = [
	{from: 37.5, to: 42.4, cam: (t, k) => ({pos: lerp3([8, 40, 62], [6, 38, 60], k), target: [20, 4, 4], fov: 55})},
	{
		from: 42.4,
		to: 44.4,
		cam: (t) => {
			const r = reqChase(t);
			const y = reqYawChase(t);
			return {pos: [r[0] + Math.sin(y) * 7 + 1.5, 5, r[2] + Math.cos(y) * 7], target: [r[0], 4, r[2]], fov: 48};
		},
	},
	{from: 44.4, to: 46.4, cam: () => ({pos: [-5, 5.2, 6.5], target: MIKEY_P.map((v, i) => (i === 1 ? 4.3 : v)) as V3, fov: 40})},
	{from: 46.4, to: 49.4, cam: () => ({pos: [5.2, 5.2, 6.5], target: [ADE_P[0], 4.3, ADE_P[2]], fov: 40})},
	{from: 49.4, to: 53.4, cam: (t, k) => ({pos: lerp3([-2, 6.5, 20], [-1, 6, 19], k), target: lerp3([0, 8, 2], [4, 4, 6], ease(range(t, 49.4, 51.2))), fov: 48})},
	{from: 53.4, to: 57.0, cam: (t, k) => ({pos: lerp3([2, 10, 34], [3, 11, 36], k), target: [16, 5, 6], fov: 58})},
	{from: 57.0, to: 60, cam: (t, k) => ({pos: lerp3([12.2, 3.2, 18.5], [12, 3.1, 18], k), target: [DONUT_REST[0], 1.0, DONUT_REST[2]], fov: 42})},
];

export const ChaseScene: React.FC<{t0: number}> = ({t0}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const stomp = hop(t) < 0.12 && t < 60 ? 0.05 : 0;
	const cam = withShake(shotAt(CHASE_SHOTS, t).cam, t, stomp);
	const rp = reqChase(t);
	const mp = millChase(t);
	const myaw = face(mp, rp);
	const kp = kliPos(t);
	const flying = t < KLI_IN[1];
	const d = donutPos(t);
	const items: BB[] = [
		{p: rp, name: 'REQ', talking: talking('req', t)},
		{p: MIKEY_P, name: 'Mikey', talking: talking('mikey', t)},
		{p: ADE_P, name: 'Ade', talking: talking('ade', t), emote: t > 46.6 && t < 49.4 ? {char: '🧮', age: (t - 46.6) % 1.4} : null},
		{p: LIA_P, name: 'Lia'},
		{p: d.p, h: d.lying > 0.5 ? 2.0 : 4.6, name: 'TheDonut', talking: talking('donut', t)},
	];
	if (t > KLI_IN[0]) items.push({p: kp, name: 'lojjkli', talking: talking('kli', t)});
	return (
		<AbsoluteFill>
			<Stage cam={cam} env={{...STORM, shadowCenter: [12, 0, 4], shadowSize: 60}}>
				<Field t={t} />
				<Clouds t={t} color="#8a90a0" opacity={0.9} />
				<GiantMill p={mp} s={BIG} yaw={myaw} spin={t * 3} tilt={Math.sin((t - 38) * Math.PI / 0.9) * 0.05} eyes={1} />
				<pointLight position={[mp[0], 22, mp[2] + 8]} color="#ff2a1a" intensity={150} distance={40} />
				<Avatar look={{...REQ_LOOK, face: 'shock'}} position={rp} rotationY={reqYawChase(t)} pose={{time: t, walk: t * 16, walkAmt: 1, armsUp: 1}} />
				<Family t={t} f="liashock" yaw={0.5} pose={(i) => ({armsUp: i === 1 || i === 4 ? 1 : 0, lean: i === 3 && t > 46.4 && t < 49.4 ? 0.3 : 0})} />
				<Pigeon position={[PIG_P[0], Y + 0.5, PIG_P[2]]} t={t} flap={0} scale={1.6} />
				<Kids t={t} yaw={(p) => face(p, rp)} pose={(i) => ({armsUp: 1, jump: Math.abs(Math.sin(t * 5 + i)) * 0.6})} />
				{t > KLI_IN[0] ? <Avatar look={flying ? KLI_LOOK : {...KLI_LOOK, wings: false}} position={kp} rotationY={flying ? 0.9 : 0.4} pose={{time: t, fly: flying ? 1 : 0, point: t > 52 && t < 53.4 ? 1 : 0}} /> : null}
				{t > KLI_IN[1] - 0.2 ? (
					<group position={d.p} rotation={[-d.lying * Math.PI * 0.5, d.spin, 0]}>
						<TalkingDonut position={[0, 0, 0]} yaw={0} scale={1.2} t={t} talk={talking('donut', t)} mood={t > BOUNCE ? 'hurt' : 'smug'} bowtie tears={t > BOUNCE + 1 ? 1 : 0} />
					</group>
				) : null}
				{t > BOUNCE && t < BOUNCE + 0.6 ? <Sparkles points={new Array(10).fill(0).map((_, i) => [d.p[0] + Math.sin(i * 2.4) * 2, d.p[1] + 2 + Math.cos(i * 2.4) * 2, d.p[2]] as V3)} t={t} color="#ffffff" size={0.5} /> : null}
			</Stage>
			<Billboards cam={cam} t={t} items={items} />
			<GameUI t={t} talking={talking('lia', t)} mode="plain" chatFrom={t0} />
			<BigText t={t} from={BOUNCE} to={BOUNCE + 1.0} text="BOING" color="#ff8fc8" top={300} size={120} />
			<BigText t={t} from={57.1} to={59.8} text="DAMAGE: 0" color="#ff4d4d" top={150} size={100} />
			<Fade t={t} inAt={t0} inDur={0.05} />
		</AbsoluteFill>
	);
};

// ================================================================ sorry, friends, the fart, the fan
const SORRY_SHOTS: Shot[] = [
	{from: 60, to: 63.6, cam: (t, k) => ({pos: lerp3([R_S[0] + 14, 6, R_S[2] + 8], [R_S[0] + 13, 6, R_S[2] + 7], k), target: [23, 10, 6], fov: 60})},
	{from: 63.6, to: 67.2, cam: (t, k) => millFaceCam(lerp(31, 29, k))},
	{from: 67.2, to: 69.4, cam: () => reqFront()},
	{from: 69.4, to: 74, cam: (t, k) => ({pos: lerp3([W_S[0] + 10, 16, W_S[2] + 46], [W_S[0] + 8, 17, W_S[2] + 44], k), target: [W_S[0], 26, W_S[2]], fov: 60})},
	// fan
	{from: 74, to: 75.6, cam: () => reqFront()},
	{from: 75.6, to: FART, cam: () => ({pos: [-2, 8, 22], target: [-4, 3, 4], fov: 52})},
	{from: FART, to: 81.2, cam: (t, k) => ({pos: lerp3([52, 10, 18], [50, 11, 20], k), target: [22, 9, 8], fov: 58})},
	{from: 81.2, to: 84.6, cam: (t, k) => millFaceCam(lerp(31, 29, k))},
	{from: 84.6, to: 87.2, cam: () => ({pos: [-2.4, 5, 1.6], target: [-3, 4.3, -3], fov: 40})},
	{from: 87.2, to: 89, cam: (t, k) => ({pos: lerp3([8, 12, 42], [8, 13, 44], k), target: [8, 5, 4], fov: 56})},
];

export const SorryScene: React.FC<{t0: number; mode: 'sorry' | 'fan'}> = ({t0, mode}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const cam = withShake(shotAt(SORRY_SHOTS, t).cam, t, t > 87.2 && t < 87.6 ? 0.08 : 0);
	const env = mode === 'sorry' ? lerpEnv(STORM, LOBBY_SUNSET, range(t, 63.6, 69.4)) : LOBBY_SUNSET;
	const mood: 'angry' | 'love' | 'happy' = t < 64.4 ? 'angry' : t > 81.2 ? 'happy' : 'love';
	const fast = mode === 'fan' ? Math.pow(Math.max(0, t - BLOW), 2) * 5 : 0;
	const spin = t * 1.4 + fast;
	const riding = t > 69.4 && t < 74;
	const reqP: V3 = riding ? bladeTip(W_S, BIG, MILL_YAW_S, spin) : R_S;
	const reqYaw = face(R_S, W_S);
	const holding = mode === 'sorry' && t > 60.3 && t < 69.4;
	const gas = mode === 'fan' && t > FART ? range(t, FART, FART + 0.9) : 0;
	const blown = mode === 'fan' ? Math.pow(Math.max(0, t - BLOW - 0.4), 2) * 3 : 0;
	const gasC: V3 = [R_S[0] + DIR[0] * blown, Y + blown * 0.3, R_S[2] + DIR[2] * blown];
	const covering = mode === 'fan' && t > 75.6 && t < BLOW + 1.6;
	const cheer = mode === 'fan' && (t > 81.2 && t < 84.6 || t > 87.2);
	const items: BB[] = [
		{p: reqP, name: 'REQ', talking: talking('req', t), hearts: riding ? (t - 69.6) % 2.5 : undefined},
		{p: LIA_P, name: 'Lia', talking: talking('lia', t)},
		{p: W_S, h: 40, name: 'THE WINDMILL', talking: talking('mill', t), hearts: mode === 'sorry' && t > 64.6 && t < 69.4 ? (t - 64.6) % 2.5 : undefined},
	];
	return (
		<AbsoluteFill>
			<Stage cam={cam} env={{...env, shadowCenter: [12, 0, 4], shadowSize: 60}}>
				<Field t={t} />
				<Clouds t={t} color={mode === 'sorry' && t < 66 ? '#8a90a0' : '#ffd6e6'} opacity={0.88} />
				<GiantMill p={W_S} s={BIG} yaw={MILL_YAW_S} spin={spin} eyes={1} mood={mood} />
				<Avatar look={{...REQ_LOOK, face: mode === 'fan' && t < 77 ? 'sick' : t > 66 || cheer ? 'grin' : 'worried'}} position={reqP} rotationY={riding ? MILL_YAW_S : reqYaw} pose={{time: t, point: holding ? 1 : 0, armsUp: riding || cheer ? 1 : 0, lean: mode === 'fan' && t < FART ? 0.2 : 0, jump: cheer ? Math.abs(Math.sin(t * 8)) * 0.6 : 0}} />
				{holding ? <Bouquet p={[R_S[0] + Math.sin(reqYaw) * 2.6 + Math.cos(reqYaw) * -1.1, 3.6, R_S[2] + Math.cos(reqYaw) * 2.6 - Math.sin(reqYaw) * -1.1]} /> : null}
				<Family t={t} f={covering ? 'liashock' : t > 84.6 && t < 87.2 ? 'liasad' : 'lia'} yaw={0.6} pose={(i) => ({cover: covering ? 1 : 0, armsUp: cheer ? 1 : 0, jump: cheer ? Math.abs(Math.sin(t * 8 + i)) * 0.6 : 0})} />
				<Pigeon position={[PIG_P[0], Y + 0.5, PIG_P[2]]} t={t} flap={cheer ? 1 : 0} scale={1.6} />
				<Kids t={t} yaw={(p) => face(p, R_S)} pose={(i) => ({cover: covering ? 1 : 0, sixSeven: cheer ? 1 : 0, jump: cheer ? Math.abs(Math.sin(t * 7 + i)) * 1.4 : 0})} />
				<Avatar look={{...KLI_LOOK, wings: false}} position={KLI_P} rotationY={0.5} pose={{time: t, cover: covering ? 1 : 0, armsUp: cheer ? 1 : 0}} />
				<group position={DONUT_REST} rotation={[-Math.PI * 0.5, 14, 0]}>
					<TalkingDonut position={[0, 0, 0]} yaw={0} scale={1.2} t={t} mood="hurt" bowtie />
				</group>
				{gas > 0 && blown < 60 ? <GasCloud center={gasC} r={2 + gas * 6} t={t} opacity={0.55} /> : null}
				{riding ? <Sparkles points={new Array(8).fill(0).map((_, i) => [reqP[0] + Math.sin(i * 2.4 + t) * 2, reqP[1] + 2 + Math.cos(i * 1.7) * 1.5, reqP[2]] as V3)} t={t} color="#ff9ad5" size={0.4} /> : null}
			</Stage>
			<Billboards cam={cam} t={t} items={items} />
			<GameUI t={t} talking={talking('lia', t)} mode="plain" chatFrom={t0} />
			{mode === 'sorry' ? (
				<>
					<BigText t={t} from={64.5} to={66.8} text="🥹" color="#fff" top={150} size={130} />
					<BigText t={t} from={70.0} to={73.6} text="🤝 BEST FRIENDS" color="#ff9ad5" top={150} size={100} />
				</>
			) : (
				<>
					<BigText t={t} from={BLOW + 0.4} to={80.6} text="🌀 FAN MODE: ON" color="#7df9ff" top={150} size={100} />
					<BigText t={t} from={87.2} to={88.8} text="NO." color="#ff4d4d" top={150} size={140} />
				</>
			)}
			<Fade t={t} inAt={t0} inDur={mode === 'fan' ? 0.05 : 0.4} outFrom={mode === 'fan' ? 88.5 : 999} outTo={mode === 'fan' ? 89 : 1000} />
		</AbsoluteFill>
	);
};

// ================================================================ end card + 69
export const EndCard3: React.FC<{t0: number}> = ({t0}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const lt = t - t0;
	const fadeOut = range(t, 94.4, 95);
	const soon = range(t, 90.9, 91.5);
	const post = t > 95.2;
	const pan = ease(range(t, 95.4, 99.2));
	const END_X = 9.8;
	const cam: Cam = withShake({pos: [lerp(-9, END_X, pan), 5.4, 9.5], target: [lerp(-9, END_X, pan), 3.4, 0], fov: t > 99.6 ? lerp(42, 30, easeOut(range(t, 99.6, 99.8))) : 42}, t, t > 99.6 && t < 100.2 ? 0.06 : 0);
	const line = useMemo(() => new Array(10).fill(0).map((_, i) => ({x: -10 + i * 2.2, i})), []);
	return (
		<AbsoluteFill style={{background: '#000'}}>
			{!post ? (
				<AbsoluteFill style={{opacity: 1 - fadeOut}}>
					<div style={{position: 'absolute', left: 0, right: 0, top: 250, display: 'flex', justifyContent: 'center', gap: 40}}>
						{['L', 'I', 'A', '3'].map((l, i) => {
							const k = ease(range(lt, 0.2 + i * 0.25, 0.6 + i * 0.25));
							return (
								<div key={l} style={{fontFamily: DOC_FONT, fontSize: 320, lineHeight: 1, color: i === 3 ? '#ff6b4a' : '#fff', opacity: k, transform: `translateY(${(1 - k) * -80}px) scale(${1.3 - 0.3 * k})`, marginLeft: i === 3 ? 50 : 0}}>
									{l}
								</div>
							);
						})}
					</div>
					<div style={{position: 'absolute', left: '50%', top: 590, width: 620 * ease(range(lt, 1.2, 1.8)), height: 5, background: '#ff6b4a', transform: 'translateX(-50%)'}} />
					<div style={{position: 'absolute', left: 0, right: 0, top: 700, textAlign: 'center', fontFamily: DOC_FONT, fontSize: 110, letterSpacing: 18, color: '#ffd6cc', opacity: soon}}>THE END... PROBABLY</div>
				</AbsoluteFill>
			) : (
				<AbsoluteFill style={{opacity: interpolate(t, [95.2, 95.5, 101.5, 102], [0, 1, 1, 0], {extrapolateRight: 'clamp'})}}>
					<Stage cam={cam} env={{...NIGHT, shadowCenter: [0, 0, 0], shadowSize: 30}}>
						<Grass />
						<House />
						<pointLight position={[0, 6, 5]} color="#ffe6c4" intensity={60} distance={24} />
						{line.map(({x, i}) =>
							i < 8 ? (
								<Avatar key={i} look={kidLook(i + 3)} position={[x, Y, 0]} scale={0.45} pose={{time: t + i}} />
							) : i === 8 ? (
								<Pigeon key={i} position={[x, Y + 0.5, 0]} t={t} flap={0} scale={1.6} />
							) : (
								<TalkingDonut key={i} position={[x, Y, 0]} scale={0.85} t={t} talk={talking('donut', t)} mood="happy" bowtie />
							),
						)}
						<Avatar look={LIA(t > 98.4 ? 'liashock' : 'lia')} position={[lerp(-8, END_X - 1.2, pan), Y, -3.2]} pose={{time: t, walk: t * 8, walkAmt: t < 99.2 ? 0.6 : 0, point: 1}} />
					</Stage>
					<Billboards cam={cam} t={t} items={[{p: [END_X, Y, 0], h: 3.4, name: 'Kid #69?', talking: talking('donut', t)}]} />
					<Vignette amt={0.9} />
				</AbsoluteFill>
			)}
			<Grain t={t} opacity={0.06} />
			<Letterbox />
		</AbsoluteFill>
	);
};
