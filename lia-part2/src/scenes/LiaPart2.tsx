import React, {useMemo} from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {ADE_LOOK, Avatar, BOOMP_LOOK, kidLook, KLI_LOOK, LIA_LOOK, Look, MIKEY_LOOK, REQ_LOOK} from '../three/Avatar';
import {Cam, clamp01, ease, easeOut, lerp, lerp3, range, V3} from '../three/cam';
import {Machine, Pet, Sparkles, Spotlight} from '../three/Props';
import {Clouds, Env, Stage} from '../three/World';
import {DutchFlag, Lobby, LOBBY_DAY, LOBBY_NIGHT, LOBBY_SUNSET, StinkPuffs, Tulips, Windmill} from '../three/MM2World';
import {baseplateTexture, CashRain, Pigeon, TalkingDonut} from '../three/KliProps';
import {rand, signTexture} from '../three/textures';
import {FALL, FART, FPS, JACKPOT, SPIN, talking} from '../timeline';
import {Billboards, BB} from '../ui/Billboards';
import {DOC_FONT, GAME_FONT, UI_FONT} from '../ui/HUD';
import {BigText, GameUI} from '../ui/MM2';
import {Fade, Flash, PopWords} from '../ui/KliUI';
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
const CASINO: Env = {...LOBBY_NIGHT, skyTop: '#05000a', skyHorizon: '#1a0630', sunIntensity: 0.35, hemiSky: '#6a3a8a', hemiIntensity: 0.55, fog: ['#12041f', 30, 90], sunGlow: 0};
const PARTY: Env = {...LOBBY_NIGHT, hemiSky: '#8a9ad0', hemiIntensity: 1.3, sunIntensity: 1.7};
const Y = 0.4;

const KID67: Look = {...kidLook(67), hat: 'cap', hatColor: '#e53935', hair: undefined, face: 'grin'};
const LIA = (f: Look['face']): Look => ({...LIA_LOOK, face: f});

// ================================================================ the Dutch home
const Grass: React.FC = () => (
	<mesh position={[0, -0.1, 0]} receiveShadow>
		<boxGeometry args={[500, 1, 500]} />
		<meshStandardMaterial map={baseplateTexture('richgrass', '#4f9a3a', '#468a33', 120)} roughness={0.9} />
	</mesh>
);

const House: React.FC<{party?: boolean}> = ({party}) => {
	const banner = useMemo(() => signTexture('67 KIDS PARTY 🎉', '#ff4fa0', '#fff36b', 'party67'), []);
	return (
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
					<meshStandardMaterial color="#fff2b0" emissive="#ffd86b" emissiveIntensity={party ? 1.2 : 0.3} />
				</mesh>
			))}
			<mesh position={[0, 1.8, 4.02]}>
				<planeGeometry args={[2.4, 3.6]} />
				<meshStandardMaterial color="#2f5d3a" />
			</mesh>
			{party ? (
				<mesh position={[0, 10.8, 4.1]}>
					<planeGeometry args={[12, 3]} />
					<meshStandardMaterial map={banner} emissive="#ffffff" emissiveMap={banner} emissiveIntensity={0.9} />
				</mesh>
			) : null}
		</group>
	);
};

const MILL: V3 = [18, 0, -24];
const DutchHome: React.FC<{t: number; party?: boolean; fall?: number}> = ({t, party, fall = 0}) => (
	<>
		<Grass />
		<House party={party} />
		<group position={MILL} rotation={[0, 0, -fall * Math.PI * 0.5]}>
			<Windmill position={[0, 0, 0]} t={t} s={1.3} rotationY={-0.5} />
		</group>
		<Windmill position={[-30, 0, -40]} t={t + 2} s={1.1} rotationY={0.3} />
		<Tulips center={[-19, 0, 2]} w={12} d={8} rows={6} />
		<Tulips center={[22, 0, 4]} w={10} d={8} rows={6} />
		<DutchFlag position={[-10, 0, -6]} t={t} />
	</>
);

// 66 kids in a loose grid; kid 67 lives elsewhere
const KIDS: {p: V3; i: number}[] = (() => {
	const out: {p: V3; i: number}[] = [];
	for (let r = 0; r < 6; r++)
		for (let c = 0; c < 11; c++) {
			const i = r * 11 + c;
			out.push({p: [-10 + c * 2 + (rand(i) - 0.5) * 0.7, Y, 3 + r * 2.1 + (rand(i + 50) - 0.5) * 0.6], i});
		}
	return out;
})();

const Kids: React.FC<{t: number; look: (p: V3, n: number) => number; pose: (n: number) => Record<string, number>; offset?: (p: V3, n: number) => V3}> = ({t, look, pose, offset}) => {
	const looks = useMemo(() => KIDS.map((k) => kidLook(k.i)), []);
	return (
		<>
			{KIDS.map((k, n) => {
				const p = offset ? offset(k.p, n) : k.p;
				return <Avatar key={k.i} look={looks[n]} position={p} scale={0.45} rotationY={look(p, n)} pose={{time: t + n * 0.37, ...pose(n)}} />;
			})}
		</>
	);
};

// ================================================================ cold open
export const ColdOpen2: React.FC = () => {
	const t = useCurrentFrame() / FPS;
	const k = ease(range(t, 0, 10));
	const cam: Cam = {pos: lerp3([0, 5.5, 13], [3, 5, 16], k), target: lerp3([0, 3.6, 0], [-1, 3.4, 0], k), fov: 42};
	const title = range(t, 4.9, 5.4);
	const sub = range(t, 5.6, 6.2);
	const out = range(t, 9.5, 10);
	const ring = useMemo(() => new Array(14).fill(0).map((_, i) => ({a: (i / 14) * Math.PI * 2, i})), []);
	return (
		<AbsoluteFill style={{background: '#000'}}>
			<Stage cam={cam} env={VOID}>
				<mesh position={[0, -0.25, 0]} receiveShadow>
					<cylinderGeometry args={[6, 6.3, 0.5, 48]} />
					<meshStandardMaterial color="#2a1f2c" roughness={0.3} metalness={0.4} />
				</mesh>
				<Spotlight position={[0, 22, 3]} target={[0, 0, 0]} intensity={1600} color="#ffe6f4" />
				<pointLight position={[2, 5, 7]} color="#ffdcef" intensity={30} distance={16} />
				<Avatar look={LIA('hearts')} position={[-1.2, 0, 0]} rotationY={0.2} pose={{time: t}} />
				<Avatar look={BOOMP_LOOK} position={[1.2, 0, 0]} rotationY={-0.2} pose={{time: t + 1}} />
				{ring.map(({a, i}) => {
					const s = clamp01((t - 1.0 - i * 0.12) / 0.25);
					if (s <= 0) return null;
					return <Avatar key={i} look={kidLook(i)} position={[Math.sin(a) * 4.4, 0, Math.cos(a) * 3.2 - 0.6]} scale={0.45 * s} rotationY={a + Math.PI} pose={{time: t + i, sixSeven: 1, jump: Math.abs(Math.sin(t * 6 + i)) * 1.2}} />;
				})}
			</Stage>
			<Vignette />
			<div style={{position: 'absolute', left: 120, top: 90, fontFamily: DOC_FONT, fontSize: 80, letterSpacing: 16, color: '#ffd6ec', opacity: interpolate(t, [0.4, 0.8, 4.2, 4.6], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}}>
				LAST TIME...
			</div>
			<div style={{position: 'absolute', left: 150, top: 330, opacity: title, transform: `translateX(${(1 - title) * -40}px)`}}>
				<div style={{fontFamily: DOC_FONT, fontSize: 300, color: '#fff', letterSpacing: 40, lineHeight: 1}}>LIA 2</div>
				<div style={{height: 4, width: 640 * title, background: '#ff9ad5', marginTop: 10}} />
				<div style={{fontFamily: UI_FONT, fontSize: 40, color: '#ffd6ec', marginTop: 24, letterSpacing: 10, opacity: sub, fontWeight: 600}}>67 PROBLEMS</div>
			</div>
			<Flash t={t} at={7.2} dur={0.5} />
			<BigText t={t} from={7.4} to={9.6} text="✅ EVERYONE RESPAWNED" color="#9cff8a" top={820} size={70} />
			<Grain t={t} />
			<Letterbox h={110 * (1 - out)} />
			<AbsoluteFill style={{background: '#000', opacity: Math.max(1 - t / 0.7, out)}} />
		</AbsoluteFill>
	);
};

// ================================================================ home: dinner, count, panic
const LIA_H: V3 = [-3, Y, -5];
const BOOMP_H: V3 = [3, Y, -5];
const HOME_SHOTS: Shot[] = [
	{from: 10, to: 16.2, cam: (t, k) => ({pos: lerp3([32, 22, 42], [24, 15, 32], ease(k)), target: [0, 3, -4], fov: 50})},
	{from: 16.2, to: 18.0, cam: (t, k) => ({pos: lerp3([7, 5.8, 6], [6.6, 5.7, 5.2], k), target: [2.4, 4.4, -5], fov: 40})},
	{from: 18.0, to: 20.0, cam: (t, k) => ({pos: lerp3([0, 7.5, -2.5], [0, 7, -1.5], k), target: [0, 1.4, 10], fov: 56})},
	{from: 20.0, to: 24.0, cam: (t, k) => ({pos: lerp3([-1.2, 5.0, 2.4], [-1.6, 4.9, 1.4], k), target: [-3, 4.3, -5], fov: 40})},
	{from: 24.0, to: 26.4, cam: (t, k) => ({pos: [-2.2, 4.7, -0.2], target: [-3, 4.4, -5], fov: lerp(40, 26, easeOut(range(t, 24.0, 24.2)))})},
	{from: 26.4, to: 29, cam: (t, k) => ({pos: lerp3([0, 14, 28], [0, 17, 32], k), target: [0, 2, 2], fov: 50})},
];

export const HomeScene: React.FC<{t0: number}> = ({t0}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const cam = withShake(shotAt(HOME_SHOTS, t).cam, t, t > 24.0 && t < 24.6 ? 0.08 : 0);
	const six = t > 18.0 && t < 20.0;
	const panic = t > 26.4;
	const lf: Look['face'] = t > 24.0 ? 'liashock' : 'lia';
	const items: BB[] = [
		{p: LIA_H, name: 'Lia', talking: talking('lia', t)},
		{p: BOOMP_H, name: 'BoompjeJunior', talking: talking('boomp', t)},
	];
	const n = t < 21.5 ? '' : t < 22.3 ? '64' : t < 23.1 ? '65' : t < 24.0 ? '66' : '67?';
	return (
		<AbsoluteFill>
			<Stage cam={cam} env={{...LOBBY_SUNSET, shadowCenter: [0, 0, 0], shadowSize: 40}}>
				<DutchHome t={t} />
				<Clouds t={t} color="#ffd6e6" opacity={0.85} />
				<Avatar look={LIA(lf)} position={LIA_H} rotationY={0.1} pose={{time: t, point: t > 20.0 && t < 24.0 ? 1 : 0, armsUp: panic ? 1 : 0, jump: panic ? Math.abs(Math.sin(t * 9)) * 0.4 : 0}} />
				<Avatar look={BOOMP_LOOK} position={BOOMP_H} rotationY={-0.1} pose={{time: t + 1, wave: t > 16.2 && t < 18 ? 1 : 0, headYaw: panic ? Math.sin(t * 5) * 0.6 : 0}} />
				<Kids
					t={t}
					look={(p, i) => (panic ? face(p, LIA_H) + Math.sin(t * 4 + i) * 0.8 : face(p, [0, Y, -5]))}
					pose={(i) => ({sixSeven: six ? 1 : 0, jump: six ? Math.abs(Math.sin(t * 7 + i)) * 1.6 : 0, headYaw: panic ? Math.sin(t * 6 + i) * 0.7 : 0})}
				/>
			</Stage>
			<Billboards cam={cam} t={t} items={items} />
			<GameUI t={t} talking={talking('lia', t)} mode="plain" chatFrom={t0} />
			{t > 21.5 && t < 26.4 ? (
				<div style={{position: 'absolute', right: 160, top: 240, fontFamily: GAME_FONT, fontWeight: 700, fontSize: 200, color: n === '67?' ? '#ff4d4d' : '#fff', WebkitTextStroke: '26px #121212', paintOrder: 'stroke fill', transform: `rotate(${n === '67?' ? -8 : 4}deg)`}}>
					{n}
				</div>
			) : null}
			<BigText t={t} from={18.0} to={19.8} text="SIX 🤲 SEVEN" color="#ffd23f" top={160} size={110} />
			<BigText t={t} from={26.6} to={28.9} text="KIDS: 66/67 ⚠️" color="#ff4d4d" top={160} size={100} />
			<Fade t={t} inAt={t0} outFrom={28.6} outTo={29} />
		</AbsoluteFill>
	);
};

// ================================================================ lobby: the search
const LIA_L: V3 = [0, Y, 6];
const MIKEY_L: V3 = [3.5, Y, 8];
const ADE_L: V3 = [-3.5, Y, 8];
const WALK = 35.4;
const walkZ = (t: number) => Math.max(0, t - WALK) * 4.2;
const PRINTS = new Array(13).fill(0).map((_, i) => ({p: [-3.5 + (i % 2 ? 0.45 : -0.45), Y + 0.03, 4 - i * 1.6] as V3, at: WALK - 0.4 + i * 0.12}));

const LOBBY_SHOTS: Shot[] = [
	{from: 29, to: 32.4, cam: (t, k) => ({pos: lerp3([0, 6.2, 21], [0, 6, 19.5], k), target: [0, 4, 6.5], fov: 44})},
	{from: 32.4, to: 35.0, cam: (t, k) => ({pos: lerp3([-1.2, 4.8, 14], [-1.6, 4.6, 13.2], k), target: [-3.5, 3.8, 8], fov: 40})},
	{from: 35.0, to: 38.0, cam: (t) => ({pos: [1.5, 9, 14 - walkZ(t)], target: [-3.5, 0.5, 2 - walkZ(t)], fov: 50})},
	{from: 38.0, to: 40.2, cam: (t, k) => ({pos: lerp3([1.5, 9, 4], [0.5, 8, -2], ease(k)), target: [-3.5, 4, -17], fov: 50})},
];

export const LobbyScene: React.FC<{t0: number}> = ({t0}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const cam = shotAt(LOBBY_SHOTS, t).cam;
	const wz = walkZ(t);
	const walking = t > WALK;
	const at = (p: V3): V3 => [p[0], p[1], p[2] - wz];
	const sign = useMemo(() => signTexture('🎰 CASINO', '#3a0050', '#ff5bd6', 'casino'), []);
	const items: BB[] = [
		{p: at(LIA_L), name: 'Lia', talking: talking('lia', t)},
		{p: at(MIKEY_L), name: 'Mikey', talking: talking('mikey', t)},
		{p: at(ADE_L), name: 'Ade', talking: talking('ade', t), emote: t > 33.0 ? {char: '🔍', age: (t - 33.0) % 1.6} : null},
	];
	const wp = (o: number) => ({time: t + o, walk: t * 10 + o, walkAmt: walking ? 1 : 0});
	return (
		<AbsoluteFill>
			<Stage cam={cam} env={{...LOBBY_DAY, shadowCenter: [0, 0, 4 - wz], shadowSize: 30}}>
				<Lobby t={t} />
				<Clouds t={t} />
				<Avatar look={LIA('liasad')} position={at(LIA_L)} rotationY={walking ? Math.PI : 0} pose={wp(0)} />
				<Avatar look={MIKEY_LOOK} position={at(MIKEY_L)} rotationY={walking ? Math.PI : -0.3} pose={wp(1)} />
				<Avatar look={ADE_LOOK} position={at(ADE_L)} rotationY={walking ? Math.PI : 0.3} pose={{...wp(2), lean: t > 32.4 ? 0.45 : 0}} />
				{PRINTS.map((f, i) =>
					t > f.at ? (
						<mesh key={i} position={f.p} rotation={[-Math.PI / 2, 0, 0]} scale={[0.32, 0.55, 1]}>
							<circleGeometry args={[1, 16]} />
							<meshStandardMaterial color="#ffd84d" emissive="#ffb300" emissiveIntensity={1.4} transparent opacity={0.9} depthWrite={false} />
						</mesh>
					) : null,
				)}
				<group position={[-3.5, Y, -17]}>
					<mesh position={[0, 4, -0.3]} castShadow>
						<boxGeometry args={[8, 8, 0.6]} />
						<meshStandardMaterial color="#2a0838" roughness={0.4} />
					</mesh>
					<mesh position={[0, 2.6, 0.02]}>
						<planeGeometry args={[3, 5.2]} />
						<meshStandardMaterial color="#ff5bd6" emissive="#ff5bd6" emissiveIntensity={1.5} />
					</mesh>
					<mesh position={[0, 6.6, 0.02]}>
						<planeGeometry args={[7.6, 1.9]} />
						<meshStandardMaterial map={sign} emissive="#ffffff" emissiveMap={sign} emissiveIntensity={1.1} />
					</mesh>
					<pointLight position={[0, 3, 2]} color="#ff5bd6" intensity={80} distance={16} />
				</group>
			</Stage>
			<Billboards cam={cam} t={t} items={items} />
			<GameUI t={t} talking={talking('lia', t)} mode="plain" chatFrom={t0} />
			<Fade t={t} inAt={t0} />
		</AbsoluteFill>
	);
};

// ================================================================ casino
const REQ_C: V3 = [3.4, 0.05, 6.8];
const STOOL: V3 = [-0.6, 0, 5.6];
const KID_C: V3 = [STOOL[0], 2.2, STOOL[2]];
const ENTER = 40.2;
const crew = (t: number, x: number): V3 => [x, 0.05, lerp(24, 13.5, ease(range(t, ENTER, ENTER + 1.8)))];
const LIA_X = 0;
const DRAGON0: V3 = [0, 7, 3];
const DRAGON1: V3 = [-2.4, 4.0, 6.6];

const reelSpin = (t: number, i: number) => {
	const stop = [49.4, 49.9, JACKPOT][i];
	if (t < SPIN) return i * 1.3 + 0.4;
	if (t >= stop) return 2;
	return 2 + (stop - t) * 9 * (1 + i * 0.2);
};

const CASINO_SHOTS: Shot[] = [
	{from: 40.2, to: 42.8, cam: (t, k) => ({pos: lerp3([5.4, 5.2, 11.5], [5.2, 5.0, 11], k), target: [3.4, 4.4, 6.8], fov: 40})},
	{from: 42.8, to: 44.6, cam: (t, k) => ({pos: lerp3([0.8, 4.4, 10], [0.6, 4.3, 9.4], k), target: [-0.6, 3.6, 5.6], fov: 40})},
	{from: 44.6, to: 45.8, cam: (t) => ({pos: [1.0, 4.9, 9.0], target: [0, 4.3, 13.5], fov: 40})},
	{from: 45.8, to: 49.0, cam: (t, k) => ({pos: lerp3([12, 7, 17], [11, 7.2, 16], k), target: [1, 6, 4], fov: 50})},
	{from: 49.0, to: JACKPOT, cam: () => ({pos: [0, 8.6, 12.5], target: [0, 8.6, 2], fov: 34})},
	{from: JACKPOT, to: 53.6, cam: (t, k) => ({pos: lerp3([0, 13, 27], [0, 14, 30], k), target: [0, 7, 4], fov: 54})},
	{from: 53.6, to: 56.4, cam: (t, k) => ({pos: lerp3([-5.5, 4.2, 12.5], [-5.2, 4.1, 12], k), target: [-1.4, 3.4, 6], fov: 42})},
	{from: 56.4, to: 58.5, cam: (t, k) => ({pos: lerp3([1.0, 4.7, 9.0], [0.7, 4.6, 10.2], k), target: [0, 4.3, 13.5], fov: 40})},
];

export const CasinoScene: React.FC<{t0: number}> = ({t0}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const cam = withShake(shotAt(CASINO_SHOTS, t).cam, t, t > JACKPOT && t < JACKPOT + 0.8 ? 0.12 : 0);
	const won = t > JACKPOT;
	const dk = ease(range(t, 51.0, 52.4));
	const dragonP = lerp3(DRAGON0, DRAGON1, dk);
	const liaP = crew(t, LIA_X);
	const liaFace: Look['face'] = t > 56.4 ? 'liasad' : t > 44.4 ? 'liashock' : 'lia';
	const askMom = t > 42.8 && t < 44.4 ? face(KID_C, liaP) : t > 53.4 ? face(KID_C, liaP) : Math.PI;
	const reqYaw = t > ENTER && t < 44.4 ? face(REQ_C, liaP) : t > 45.8 && t < 49 ? face(REQ_C, liaP) : Math.PI;
	const items: BB[] = [
		{p: REQ_C, name: 'REQ', talking: talking('req', t)},
		{p: [KID_C[0], KID_C[1] - 0.2, KID_C[2]], h: 3.0, name: 'Kid #67', talking: talking('kid', t)},
		{p: liaP, name: 'Lia', talking: talking('lia', t)},
	];
	return (
		<AbsoluteFill>
			<Stage cam={cam} env={{...CASINO, shadowCenter: [0, 0, 8], shadowSize: 30}}>
				<Machine t={t} spin={[reelSpin(t, 0), reelSpin(t, 1), reelSpin(t, 2)]} lights={won ? 1.6 : 1} />
				<mesh position={[STOOL[0], 1.1, STOOL[2]]} castShadow>
					<cylinderGeometry args={[0.8, 0.9, 2.2, 16]} />
					<meshStandardMaterial color="#b0123e" roughness={0.4} />
				</mesh>
				<Avatar look={KID67} position={KID_C} scale={0.45} rotationY={askMom} pose={{time: t, point: t > SPIN - 0.3 && t < SPIN + 1 ? 1 : 0, armsUp: won && t < 53.4 ? 1 : 0, jump: won && t < 53.4 ? Math.abs(Math.sin(t * 9)) * 0.8 : 0}} />
				<Avatar look={{...REQ_LOOK, face: 'grin'}} position={REQ_C} rotationY={reqYaw} pose={{time: t + 1, point: t > 41 && t < 42.3 ? 1 : 0, armsUp: (t > 45.8 && t < 49) || (won && t < 53.6) ? 1 : 0, jump: won && t < 53.6 ? Math.abs(Math.sin(t * 8)) * 0.8 : 0}} />
				<Avatar look={LIA(liaFace)} position={liaP} rotationY={Math.PI} pose={{time: t, walk: t * 10, walkAmt: t < ENTER + 1.8 ? 1 : 0, armsUp: t > 44.6 && t < 45.8 ? 1 : 0}} />
				<Avatar look={BOOMP_LOOK} position={crew(t, 3.2)} rotationY={Math.PI} pose={{time: t + 2, walk: t * 10 + 1, walkAmt: t < ENTER + 1.8 ? 1 : 0}} />
				<Avatar look={MIKEY_LOOK} position={crew(t, -3.4)} rotationY={Math.PI} pose={{time: t + 3, walk: t * 10 + 2, walkAmt: t < ENTER + 1.8 ? 1 : 0, armsUp: won && t < 53.6 ? 1 : 0}} />
				<Avatar look={ADE_LOOK} position={crew(t, 6.4)} rotationY={Math.PI} pose={{time: t + 4, walk: t * 10 + 3, walkAmt: t < ENTER + 1.8 ? 1 : 0, armsUp: won && t < 53.6 ? 1 : 0}} />
				{t > 51.0 ? (
					<>
						<Pet kind="dragon" gold position={[dragonP[0], dragonP[1] - 1.6, dragonP[2]]} rotationY={0.3} t={t} scale={lerp(0.2, 0.75, dk)} />
						<pointLight position={[dragonP[0], dragonP[1] + 1, dragonP[2] + 1.5]} color="#ffd23f" intensity={30} distance={8} />
						<Sparkles points={new Array(10).fill(0).map((_, i) => [dragonP[0] + Math.sin(i * 2.3 + t) * 1.4, dragonP[1] + Math.cos(i * 1.7 + t * 2) * 0.9, dragonP[2] + Math.cos(i * 2.3) * 1.2] as V3)} t={t} />
					</>
				) : null}
				{won && t < 56 ? <CashRain t={t - JACKPOT} center={[0, 0, 7]} count={90} area={18} /> : null}
				<Spotlight position={[0, 20, 16]} target={[0, 2, 8]} intensity={700} color="#ffd9f2" />
			</Stage>
			<Billboards cam={cam} t={t} items={items} />
			<GameUI t={t} talking={talking('lia', t)} mode="plain" chatFrom={t0} />
			<PopWords t={t} until={48.9} words={[{at: 46.4, text: '99%', color: '#ffd23f', x: 1300, y: 260, rot: -8}, {at: 47.6, text: 'BIG WIN', color: '#7df9ff', x: 1380, y: 420, rot: 6}]} />
			<Flash t={t} at={JACKPOT} dur={0.5} color="#fff3b0" />
			<BigText t={t} from={JACKPOT + 0.1} to={51.6} text="7 7 7 JACKPOT!!!" color="#ffd23f" top={150} size={120} />
			<BigText t={t} from={51.7} to={53.5} text="🐉 GOLDEN DRAGON" color="#ffd23f" top={150} size={100} />
			<Fade t={t} inAt={t0} inDur={0.05} outFrom={58.0} outTo={58.5} />
		</AbsoluteFill>
	);
};

// ================================================================ the party
const LIA_P: V3 = [-3, Y, -5];
const BOOMP_P: V3 = [3, Y, -5];
const REQ_P: V3 = [0, Y, 9.2];
const KLI_LAND: V3 = [-4, Y, 19];
const DONUT_P: V3 = [-9, Y, 20];
const KID67_P: V3 = [9.5, Y, 16];
const KLI_IN = [61.4, 63.0];
const DONUT_IN = [66.0, 67.6];
const SWARM = 70.0;
const FREEZE = 72.6;

const kliPos = (t: number): V3 => (t < KLI_IN[1] ? lerp3([-40, 34, 50], KLI_LAND, easeOut(range(t, KLI_IN[0], KLI_IN[1]))) : KLI_LAND);
const donutPos = (t: number): V3 => {
	const k = range(t, DONUT_IN[0], DONUT_IN[1]);
	const p = lerp3([-30, Y, 22], DONUT_P, k);
	return [p[0], p[1] + (k > 0 && k < 1 ? Math.abs(Math.sin(k * Math.PI * 5)) * 1.4 : 0), p[2]];
};

const PARTY_SHOTS: Shot[] = [
	{from: 58.5, to: 61.4, cam: (t, k) => ({pos: lerp3([28, 18, 40], [22, 14, 33], ease(k)), target: [0, 2, 4], fov: 50})},
	{from: 61.4, to: 63.4, cam: (t) => ({pos: [8, 7, 36], target: lerp3(kliPos(t), [KLI_LAND[0], 4, KLI_LAND[2]], 0.4), fov: 50})},
	{from: 63.4, to: 66.0, cam: (t, k) => ({pos: lerp3([-2.4, 5.4, 26], [-2.8, 5.3, 25], k), target: [-4, 4.4, 19], fov: 40})},
	{from: 66.0, to: 68.0, cam: (t) => ({pos: [-4.5, 4.5, 31], target: [donutPos(t)[0] * 0.6 - 3, 2.8, 20], fov: 48})},
	{from: 68.0, to: SWARM, cam: (t, k) => ({pos: lerp3([-7.2, 3.6, 27.5], [-7.4, 3.5, 26.6], k), target: [-9, 2.8, 20], fov: 40})},
	{from: SWARM, to: FREEZE, cam: (t, k) => ({pos: lerp3([16, 10, 36], [14, 9, 34], k), target: [-4, 2, 14], fov: 50})},
	{from: FREEZE, to: 75.0, cam: (t, k) => ({pos: lerp3([2.6, 5.4, 17.5], [2.2, 5.3, 16.6], k), target: [0, 4.0, 9.2], fov: 40})},
	{from: 75.0, to: 76.0, cam: () => ({pos: [0, 13, 33], target: [0, 2, 8], fov: 50})},
	{from: 76.0, to: 77.0, cam: () => ({pos: [-2.2, 4.8, 0], target: [-3, 4.3, -5], fov: 40})},
	{from: 77.0, to: 80.0, cam: (t, k) => ({pos: lerp3([0, 5.6, 24], [0, 5.2, 16.5], ease(range(t, 77, FART))), target: [0, 4.0, 9.2], fov: 40})},
	{from: 80.0, to: 83.6, cam: (t, k) => ({pos: lerp3([16, 9, 30], [15, 8.6, 28], k), target: [0, 2.4, 8], fov: 50})},
	{from: 83.6, to: 84.8, cam: () => ({pos: [2.2, 5.3, 16.5], target: [0, 4.0, 9.2], fov: 40})},
	{from: 84.8, to: 88.0, cam: (t, k) => ({pos: lerp3([32, 7, 12], [33, 7.5, 13], k), target: lerp3([18, 12, -24], [26, 5, -24], ease(range(t, FALL, FALL + 2))), fov: 52})},
	{from: 88.0, to: 92, cam: (t, k) => ({pos: lerp3([-2, 12, 30], [-3, 13, 32], k), target: [18, 2, -18], fov: 52})},
];

export const PartyScene: React.FC<{t0: number}> = ({t0}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const cam = withShake(shotAt(PARTY_SHOTS, t).cam, t, (t > 75.0 && t < 75.8) || (t > FALL + 2 && t < FALL + 2.8) ? 0.12 : 0);
	const fall = Math.pow(range(t, FALL, FALL + 2.0), 2.2);
	const frozen = t > FREEZE && t < 80.0;
	const brace = t > 75.0 && t < 80.0;
	const confused = t > 80.0;
	const swarm = ease(range(t, SWARM, SWARM + 1.2)) * (1 - ease(range(t, FREEZE, FREEZE + 0.6)));
	const dancing = t < FREEZE && !(t > 66 && t < SWARM);
	const disco = t < FREEZE ? 1 : 0;
	const kp = kliPos(t);
	const flying = t < KLI_IN[1];
	const dp = donutPos(t);
	const liaFace: Look['face'] = t > 75 && t < 80 ? 'liashock' : confused ? 'liasad' : 'lia';
	const items: BB[] = [
		{p: LIA_P, name: 'Lia', talking: talking('lia', t)},
		{p: REQ_P, name: 'REQ', talking: talking('req', t), emote: t > 79.0 && t < 80.6 ? {char: '💨', age: t - 79.0} : null},
		{p: kp, name: 'lojjkli', talking: talking('kli', t)},
		{p: dp, h: 4.6, name: 'TheDonut', talking: talking('donut', t)},
		{p: KID67_P, h: 3.0, name: 'Kid #67'},
	];
	return (
		<AbsoluteFill>
			<Stage cam={cam} env={{...PARTY, shadowCenter: [0, 0, 6], shadowSize: 40}}>
				<DutchHome t={t} party fall={fall} />
				<Avatar look={LIA(liaFace)} position={LIA_P} rotationY={0.1} pose={{time: t, sixSeven: dancing ? 1 : 0, cover: brace ? 1 : 0, headYaw: confused ? Math.sin(t * 3) * 0.5 : 0}} />
				<Avatar look={BOOMP_LOOK} position={BOOMP_P} rotationY={-0.1} pose={{time: t + 1, sixSeven: dancing ? 1 : 0, cover: brace ? 1 : 0}} />
				<Avatar look={{...REQ_LOOK, face: t > FREEZE && t < 83.6 ? 'sick' : 'grin'}} position={REQ_P} rotationY={0} pose={{time: t + 2, sixSeven: dancing ? 1 : 0, lean: frozen ? 0.25 : 0, jump: dancing ? Math.abs(Math.sin(t * 7)) * 0.6 : 0}} />
				<Avatar look={MIKEY_LOOK} position={[-13, Y, 8]} rotationY={0.6} pose={{time: t + 3, sixSeven: dancing ? 1 : 0, cover: brace ? 1 : 0}} />
				<Avatar look={ADE_LOOK} position={[13, Y, 8]} rotationY={-0.6} pose={{time: t + 4, sixSeven: dancing ? 1 : 0, cover: brace ? 1 : 0}} />
				{t > KLI_IN[0] ? <Avatar look={flying ? KLI_LOOK : {...KLI_LOOK, wings: false}} position={kp} rotationY={flying ? 0.8 : t > 64.8 && t < 67.4 ? -0.9 : 0.2} pose={{time: t, fly: flying ? 1 : 0, point: t > 65.2 && t < 67.4 ? 1 : 0, cover: brace ? 1 : 0}} /> : null}
				{t > DONUT_IN[0] ? <TalkingDonut position={dp} yaw={0.3} scale={1.2} t={t} talk={talking('donut', t)} mood={t > 80 ? 'hurt' : 'smug'} bowtie wobble={t < DONUT_IN[1] || brace ? 1 : 0} /> : null}
				<Avatar look={KID67} position={KID67_P} scale={0.45} rotationY={-0.4} pose={{time: t, sixSeven: dancing ? 1 : 0, cover: brace ? 1 : 0}} />
				<Pet kind="dragon" gold position={[KID67_P[0] + 1.6, Y - 0.2, KID67_P[2]]} rotationY={-0.4} t={t} scale={0.75} />
				<Kids
					t={t}
					look={(p, i) => (t > KLI_IN[1] && t < SWARM + 1.2 && t > 63 ? face(p, KLI_LAND) : frozen || brace ? face(p, REQ_P) : confused ? face(p, REQ_P) + Math.sin(t * 2 + i) * 0.6 : Math.sin(i * 1.7) * 0.5)}
					pose={(i) => ({
						sixSeven: dancing ? 1 : 0,
						jump: dancing || (t > SWARM && t < FREEZE) ? Math.abs(Math.sin(t * 7 + i)) * 1.6 : 0,
						cover: brace ? 1 : 0,
						armsUp: (t > SWARM && t < FREEZE) || (t > 75 && t < 76) ? 1 : 0,
					})}
					offset={(p) => (swarm > 0 ? lerp3(p, [lerp(p[0], DONUT_P[0], 0.35), Y, lerp(p[2], DONUT_P[2], 0.3)], swarm) : p)}
				/>
				{t > FART && t < FART + 3 ? (
					<group position={[REQ_P[0], REQ_P[1] + 1.4, REQ_P[2] - 0.6]} scale={0.22}>
						<StinkPuffs position={[0, 0, 0]} k={(t - FART) * 1.2} />
					</group>
				) : null}
				{[0, 1, 2, 3].map((i) => (
					<pointLight key={i} position={[Math.sin(t * 1.3 + i * 1.6) * 12, 7, 8 + Math.cos(t * 1.1 + i * 1.6) * 8]} color={['#ff4fa0', '#4fd2ff', '#ffe14d', '#9cff8a'][i]} intensity={70 * disco} distance={22} />
				))}
				<pointLight position={[0, 8, 14]} color="#ffe6c4" intensity={40} distance={30} />
				{t > FALL + 2 && t < FALL + 4.5 ? (
					<Sparkles points={new Array(14).fill(0).map((_, i) => [MILL[0] + 6 + i * 1.2, 1 + (i % 3) * 0.8 + (t - FALL - 2) * 1.5, MILL[2] + Math.sin(i) * 3] as V3)} t={t} color="#c8b8a0" size={0.9} />
				) : null}
			</Stage>
			{frozen || brace ? <AbsoluteFill style={{background: '#1a0f00', mixBlendMode: 'saturation', opacity: 0.6}} /> : null}
			<Billboards cam={cam} t={t} items={items} />
			<GameUI t={t} talking={talking('lia', t)} mode="plain" chatFrom={t0} />
			<BigText t={t} from={63.0} to={64.6} text="lojjkli joined 😎" color="#b9b9ff" top={150} size={90} />
			<BigText t={t} from={FREEZE} to={74.8} text="⚠️ UH OH" color="#ff4d4d" top={150} size={110} />
			<BigText t={t} from={FART + 0.05} to={FART + 1.2} text="*pfft*" color="#9ae03a" top={780} size={70} />
			<BigText t={t} from={80.4} to={83.4} text="🦗 🦗 🦗" color="#fff" top={150} size={90} />
			<BigText t={t} from={88.4} to={91.6} text="🪦 R.I.P. WINDMILL" color="#e6e6e6" top={150} size={100} />
			<Fade t={t} inAt={t0} outFrom={91.4} outTo={92} />
		</AbsoluteFill>
	);
};

// ================================================================ end card + 68
export const EndCard2: React.FC<{t0: number}> = ({t0}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const lt = t - t0;
	const fadeOut = range(t, 97.4, 98);
	const soon = range(t, 93.9, 94.5);
	const post = t > 98.2;
	const pan = ease(range(t, 98.4, 101.6));
	const cam: Cam = withShake({pos: [lerp(-9, 7.6, pan), 5.4, 9.5], target: [lerp(-9, 7.6, pan), 3.4, 0], fov: t > 102.6 ? lerp(42, 30, easeOut(range(t, 102.6, 102.8))) : 42}, t, t > 102.6 && t < 103.2 ? 0.06 : 0);
	const line = useMemo(() => new Array(9).fill(0).map((_, i) => ({x: -10 + i * 2.2, i})), []);
	return (
		<AbsoluteFill style={{background: '#000'}}>
			{!post ? (
				<AbsoluteFill style={{opacity: 1 - fadeOut}}>
					<div style={{position: 'absolute', left: 0, right: 0, top: 250, display: 'flex', justifyContent: 'center', gap: 40}}>
						{['L', 'I', 'A', '2'].map((l, i) => {
							const k = ease(range(lt, 0.2 + i * 0.25, 0.6 + i * 0.25));
							return (
								<div key={l} style={{fontFamily: DOC_FONT, fontSize: 320, lineHeight: 1, color: i === 3 ? '#ff9ad5' : '#fff', opacity: k, transform: `translateY(${(1 - k) * -80}px) scale(${1.3 - 0.3 * k})`, marginLeft: i === 3 ? 50 : 0}}>
									{l}
								</div>
							);
						})}
					</div>
					<div style={{position: 'absolute', left: '50%', top: 590, width: 620 * ease(range(lt, 1.2, 1.8)), height: 5, background: '#ff9ad5', transform: 'translateX(-50%)'}} />
					<div style={{position: 'absolute', left: 0, right: 0, top: 700, textAlign: 'center', fontFamily: DOC_FONT, fontSize: 110, letterSpacing: 18, color: '#ffd6ec', opacity: soon}}>PART 3 COMING SOON</div>
				</AbsoluteFill>
			) : (
				<AbsoluteFill style={{opacity: interpolate(t, [98.2, 98.5, 104.5, 105], [0, 1, 1, 0], {extrapolateRight: 'clamp'})}}>
					<Stage cam={cam} env={{...PARTY, shadowCenter: [0, 0, 0], shadowSize: 30}}>
						<Grass />
						<House />
						<pointLight position={[0, 6, 5]} color="#ffe6c4" intensity={60} distance={24} />
						{line.map(({x, i}) =>
							i < 8 ? <Avatar key={i} look={kidLook(i + 3)} position={[x, Y, 0]} scale={0.45} pose={{time: t + i}} /> : <Pigeon key={i} position={[x, Y + 0.5, 0]} t={t} flap={0} scale={1.6} />,
						)}
						<Avatar look={LIA(t > 101.6 ? 'liashock' : 'lia')} position={[lerp(-8, 6.4, pan), Y, -3.2]} rotationY={0} pose={{time: t, walk: t * 8, walkAmt: t < 101.6 ? 0.6 : 0, point: 1}} />
					</Stage>
					<Billboards cam={cam} t={t} items={[{p: [7.6, Y, 0], h: 3.2, name: 'Kid #68?', talking: talking('pigeon', t)}]} />
					<Vignette amt={0.9} />
				</AbsoluteFill>
			)}
			<Grain t={t} opacity={0.06} />
			<Letterbox />
		</AbsoluteFill>
	);
};
