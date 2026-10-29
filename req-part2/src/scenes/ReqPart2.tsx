import React, {useMemo} from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {Avatar, KLI_DEEP, Look, REQ_LOOK} from '../three/Avatar';
import {Cam, ease, easeOut, lerp, lerp3, range, V3} from '../three/cam';
import {Machine, Pet, Sparkles, Spotlight} from '../three/Props';
import {Clouds, Diamond, Env, Forest, SpawnPad, Stage} from '../three/World';
import {LOBBY_DAY, LOBBY_NIGHT, Planet, SPACE} from '../three/MM2World';
import {baseplateTexture, Car, CashRain, GoldMansion, Pigeon} from '../three/KliProps';
import {rand} from '../three/textures';
import {FPS, JACKPOT, PECK, POOF, RESPAWN, SPIN1, SPIN2, talking, WIN_PIGEON} from '../timeline';
import {Billboards, BB} from '../ui/Billboards';
import {DOC_FONT, GAME_FONT, UI_FONT} from '../ui/HUD';
import {BigText, GameUI} from '../ui/MM2';
import {Fade, Flash, PopWords} from '../ui/KliUI';
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
const CASINO: Env = {...LOBBY_NIGHT, skyTop: '#05000a', skyHorizon: '#1a0630', sunIntensity: 0.4, hemiSky: '#6a3a8a', hemiIntensity: 0.6, fog: ['#12041f', 30, 90], sunGlow: 0};
const Y = 0.5;
const REQ = (f: Look['face']): Look => ({...REQ_LOOK, face: f});
const REQ_GOLD: Look = {...REQ_LOOK, face: 'grin', hatColor: '#d9a520', shirt: 'suit', shirtColor: '#d9a520'};

/** Pet Sim style diamonds counter, top right. */
const Diamonds: React.FC<{value: number; t: number; flash?: boolean}> = ({value, t, flash}) => (
	<div style={{position: 'absolute', right: 40, top: 30, display: 'flex', alignItems: 'center', gap: 14, padding: '10px 26px', borderRadius: 18, background: 'rgba(0,0,0,0.55)', transform: `scale(${flash ? 1 + Math.abs(Math.sin(t * 10)) * 0.08 : 1})`}}>
		<span style={{fontSize: 52, fontFamily: '"Noto Color Emoji"'}}>💎</span>
		<span style={{fontFamily: GAME_FONT, fontWeight: 700, fontSize: 56, color: value === 0 ? '#ff4d4d' : '#7df9ff', fontVariantNumeric: 'tabular-nums'}}>{Math.round(value).toLocaleString('en-US')}</span>
	</div>
);

const Grass: React.FC = () => (
	<mesh position={[0, -0.5, 0]} receiveShadow>
		<boxGeometry args={[600, 1, 600]} />
		<meshStandardMaterial map={baseplateTexture('psgrass', '#5aa83e', '#4f9a36', 140)} roughness={0.9} />
	</mesh>
);

const PETS = new Array(10).fill(0).map((_, i) => ({kind: (i % 2 ? 'cat' : 'dog') as 'cat' | 'dog', x: -16 + rand(i) * 32, z: -10 + rand(i + 20) * 26, i}));
const WanderPets: React.FC<{t: number}> = ({t}) => (
	<>
		{PETS.map((p) => {
			const a = t * 0.4 + p.i;
			return <Pet key={p.i} kind={p.kind} position={[p.x + Math.sin(a) * 2, 0, p.z + Math.cos(a) * 2]} rotationY={a + Math.PI / 2} t={t} scale={0.7} />;
		})}
	</>
);

// ================================================================ cold open
export const ColdOpen2: React.FC = () => {
	const t = useCurrentFrame() / FPS;
	const k = ease(range(t, 0, 9));
	const cam: Cam = {pos: lerp3([1.2, 5, 10], [3.6, 4.6, 14], k), target: lerp3([0.2, 4.2, 0], [-1.2, 3.9, 0], k), fov: 42};
	const title = range(t, 4.4, 4.9);
	const sub = range(t, 5.1, 5.7);
	const out = range(t, 8.5, 9);
	return (
		<AbsoluteFill style={{background: '#000'}}>
			<Stage cam={cam} env={VOID}>
				<mesh position={[0, -0.25, 0]} receiveShadow>
					<cylinderGeometry args={[5, 5.3, 0.5, 48]} />
					<meshStandardMaterial color="#2a1f1f" roughness={0.3} metalness={0.4} />
				</mesh>
				<Spotlight position={[0, 22, 3]} target={[0, 0, 0]} intensity={1600} color="#ffe6e0" />
				<pointLight position={[2, 5, 7]} color="#ffdcd0" intensity={30} distance={16} />
				<Avatar look={REQ('sad')} position={[0, 0, 0]} rotationY={0.2} pose={{time: t, headPitch: 0.25}} />
				{t > 2 ? <Diamond position={[2.2, 3 + Math.sin(t * 2) * 0.3, 0.5]} t={t} scale={0.8} /> : null}
			</Stage>
			<Vignette />
			<div style={{position: 'absolute', left: 120, top: 90, fontFamily: DOC_FONT, fontSize: 80, letterSpacing: 16, color: '#ffd6d0', opacity: interpolate(t, [0.4, 0.8, 3.8, 4.2], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}}>
				LAST TIME...
			</div>
			<div style={{position: 'absolute', left: 150, top: 330, opacity: title, transform: `translateX(${(1 - title) * -40}px)`}}>
				<div style={{fontFamily: DOC_FONT, fontSize: 300, color: '#fff', letterSpacing: 40, lineHeight: 1}}>REQ 2</div>
				<div style={{height: 4, width: 640 * title, background: '#ff5b5b', marginTop: 10}} />
				<div style={{fontFamily: UI_FONT, fontSize: 40, color: '#ffd6d0', marginTop: 24, letterSpacing: 10, opacity: sub, fontWeight: 600}}>ONE MORE SPIN</div>
			</div>
			<Grain t={t} />
			<Letterbox h={110 * (1 - out)} />
			<AbsoluteFill style={{background: '#000', opacity: Math.max(1 - t / 0.7, out)}} />
		</AbsoluteFill>
	);
};

// ================================================================ space
const BLOCK: V3 = [0, 0, 30];
export const SpaceScene: React.FC<{t0: number; post?: boolean}> = ({t0, post}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const lt = t - t0;
	const k = post ? 0.1 + lt * 0.04 : 0.3;
	const fall = post ? 0 : Math.pow(Math.max(0, t - 17.6), 2) * 6;
	const reqP: V3 = [BLOCK[0], BLOCK[1] + 0.5 - fall, BLOCK[2]];
	const cam: Cam = post
		? withShake({pos: lerp3([6, 4, 44], [5, 4.5, 41], range(lt, 0, 8)), target: [1.5, 3, 30], fov: 46}, t, t > 90.4 && t < 90.9 ? 0.06 : 0)
		: t < 15.6
			? {pos: lerp3([14, 10, 52], [8, 6, 42], ease(range(t, 9, 15.6))), target: [0, 2, 26], fov: 46}
			: {pos: [2.2, 5.2, 36], target: [0, 4 - fall * 0.5, 30], fov: 42};
	const items: BB[] = [{p: reqP, name: 'REQ', talking: talking('req', t)}];
	if (post) items.push({p: [3.2, 0.5, 30], name: 'lojjkli', talking: talking('kli', t)});
	return (
		<AbsoluteFill>
			<Stage cam={cam} env={SPACE}>
				<group position={[-20, -10, -120]}>
					<Planet k={k} t={t} />
				</group>
				<mesh position={[BLOCK[0], -0.5, BLOCK[2]]} castShadow receiveShadow rotation={[0, t * 0.1, 0]}>
					<boxGeometry args={[2.4, 1, 2.4]} />
					<meshStandardMaterial color="#5aa83e" roughness={0.8} />
				</mesh>
				<Avatar look={REQ(post ? 'grin' : t > 15.4 ? 'shock' : 'worried')} position={reqP} rotationY={post ? 0.4 : 0.2} pose={{time: t, headPitch: !post && t > 15.6 ? 0.5 : 0, armsUp: !post && t > 17.6 ? 1 : 0}} />
				{post ? (
					<>
						<mesh position={[3.2, -0.5, 30]} castShadow receiveShadow>
							<boxGeometry args={[2.4, 1, 2.4]} />
							<meshStandardMaterial color="#5aa83e" roughness={0.8} />
						</mesh>
						<Avatar look={KLI_DEEP} position={[3.2, 0.5, 30]} rotationY={-0.6} pose={{time: t + 1, point: t > 86.4 && t < 89 ? 1 : 0}} />
					</>
				) : null}
			</Stage>
			<Billboards cam={cam} t={t} items={items} />
			{!post ? (
				<>
					<GameUI t={t} talking={talking('req', t)} mode="plain" hideChat />
					<Diamonds value={0} t={t} />
					<Flash t={t} at={19.2} dur={0.4} />
				</>
			) : null}
			{post ? <Vignette amt={0.9} /> : null}
			<Fade t={t} inAt={t0} />
		</AbsoluteFill>
	);
};

// ================================================================ lobby: the promise
const REQ_L: V3 = [0, Y, 0];
const KLI_L: V3 = [3.4, Y, 1.6];
const MACH_L: V3 = [0, 0, -36];
const RUN = 43.4;
const reqLobby = (t: number): V3 => lerp3(REQ_L, [0, 0.05, -28], easeOut(range(t, RUN, 45.6)) * 0.95);

const LOBBY_SHOTS: Shot[] = [
	{from: 19.6, to: 23.0, cam: (t, k) => ({pos: lerp3([-8, 7, 16], [-7, 6.6, 15], k), target: [1, 3, 0], fov: 46})},
	{from: 23.0, to: 26.6, cam: (t, k) => ({pos: lerp3([-1.2, 5.2, 6.8], [-1.0, 5.1, 6.2], k), target: [KLI_L[0], 4.4, KLI_L[2]], fov: 40})},
	{from: 26.6, to: 28.8, cam: (t, k) => ({pos: lerp3([1.8, 5.2, 6.4], [1.6, 5.1, 6.0], k), target: [0, 4.4, 0], fov: 40})},
	{from: 28.8, to: 31.6, cam: (t, k) => ({pos: lerp3([-1.2, 2.4, 6.2], [-1.0, 2.2, 5.6], k), target: [0, 5.2, 0], fov: 46})},
	{from: 31.6, to: 34.2, cam: (t, k) => ({pos: lerp3([10, 8, 18], [9, 7.5, 17], k), target: [0, 3, 0], fov: 48})},
	{from: 34.2, to: 36.0, cam: () => ({pos: [1.2, 4.8, 4.6], target: [0, 4.4, 0], fov: 36})},
	{from: 36.0, to: 38.8, cam: (t, k) => ({pos: [1.6, 5.4, 5.5], target: [0, 8, -36], fov: lerp(34, 22, ease(k))})},
	{from: 38.8, to: 40.8, cam: () => ({pos: [1.8, 5.2, 6.0], target: [0, 4.4, 0], fov: 40})},
	{from: 40.8, to: 42.6, cam: (t, k) => ({pos: lerp3([0, 9, -20], [0, 9, -22], k), target: [0, 8.6, -36], fov: 40})},
	{from: 42.6, to: RUN, cam: () => ({pos: [0.9, 4.6, 3.6], target: [0, 4.5, 0], fov: 30})},
	{from: RUN, to: 45.6, cam: (t) => ({pos: [7, 6, 10], target: [0, 3, reqLobby(t)[2] * 0.6], fov: 50})},
];

export const LobbyScene: React.FC<{t0: number}> = ({t0}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const cam = withShake(shotAt(LOBBY_SHOTS, t).cam, t, t > 34.2 && t < 34.6 ? 0.05 : 0);
	const rp = reqLobby(t);
	const running = t > RUN;
	const call = range(t, 35.6, 36.4);
	const rf: Look['face'] = t > 42.6 ? 'grin' : t > 38.8 && t < 40.8 ? 'angry' : t > 34.2 ? 'worried' : t > 28.8 && t < 31.6 ? 'happy' : 'smile';
	const items: BB[] = [
		{p: rp, name: 'REQ', talking: talking('req', t), emote: t > 34.4 && t < 36 ? {char: '💦', age: t - 34.4} : null},
		{p: KLI_L, name: 'lojjkli', talking: talking('kli', t)},
	];
	return (
		<AbsoluteFill>
			<Stage cam={cam} env={{...LOBBY_DAY, shadowCenter: [0, 0, -6], shadowSize: 40}}>
				<Grass />
				<Clouds t={t} />
				<Forest count={40} radius={[40, 140]} />
				<SpawnPad position={[0, 0, 0]} />
				<WanderPets t={t} />
				<group position={MACH_L}>
					<Machine t={t} spin={[0.4, 1.7, 3.1]} lights={1 + call * 1.5} />
				</group>
				{call > 0 ? <pointLight position={[0, 9, -28]} color="#ff5bd6" intensity={200 * call} distance={40} /> : null}
				<Avatar look={REQ(rf)} position={rp} rotationY={running ? Math.PI : t > 36 && t < 38.8 ? Math.PI : face(REQ_L, KLI_L) * (t > 23 && t < 28.8 ? 1 : 0)} pose={{time: t, walk: t * 16, walkAmt: running ? 1 : 0, headPitch: t > 28.8 && t < 31.6 ? -0.3 : 0, sixSeven: t > 28.8 && t < 31.6 ? 0 : 0, cover: t > 38.8 && t < 40.4 ? 1 : 0}} />
				<Avatar look={KLI_DEEP} position={KLI_L} rotationY={t > 23 && t < 26.6 ? face(KLI_L, [-1.2, 0, 6.8]) : face(KLI_L, rp)} pose={{time: t + 1, armsUp: t > 43.6 ? 1 : 0, point: t > 23 && t < 24.6 ? 1 : 0}} />
				{t > 28.8 && t < 31.6 ? <Sparkles points={new Array(10).fill(0).map((_, i) => [Math.sin(i * 2.4) * 1.6, 2 + i * 0.5, Math.cos(i * 2.4) * 1.6] as V3)} t={t} color="#fff2a8" size={0.3} /> : null}
			</Stage>
			<Billboards cam={cam} t={t} items={items} />
			<GameUI t={t} talking={talking('req', t)} mode="plain" chatFrom={t0} />
			<Diamonds value={0} t={t} flash={t > 23 && t < 26.6} />
			<BigText t={t} from={31.7} to={34.0} text="DAY 1 WITHOUT GAMBLING 🙏" color="#9cff8a" top={150} size={80} />
			<BigText t={t} from={34.3} to={36.0} text="⏱️ MINUTE 3" color="#ff4d4d" top={150} size={100} />
			<BigText t={t} from={40.9} to={42.5} text="🎁 FREE SPIN" color="#ff5bd6" top={150} size={110} />
			{t > 36 && t < 38.8 ? <AbsoluteFill style={{background: 'radial-gradient(circle at 50% 45%, rgba(255,91,214,0.0) 30%, rgba(80,0,60,0.55) 100%)'}} /> : null}
			<Flash t={t} at={RESPAWN} dur={0.5} />
			<Fade t={t} inAt={t0} inDur={0.01} />
		</AbsoluteFill>
	);
};

// ================================================================ the machine: pigeon, jackpot
const REQ_M: V3 = [2.2, 0.05, 7.2];
const PIG_M: V3 = [-2.4, 2.0, 3.6];
const reel = (t: number, i: number, from: number, stop: number[], land: number) => {
	const s = stop[i];
	const end = from + 2.2 + i * 0.4;
	if (t < from) return land - 3 + i;
	if (t >= end) return land;
	return land + (end - t) * 9;
};

const MACHINE_SHOTS: Shot[] = [
	{from: 45.6, to: WIN_PIGEON, cam: (t, k) => ({pos: lerp3([11, 7, 18], [10, 7.2, 17], k), target: [0, 7, 2], fov: 50})},
	{from: WIN_PIGEON, to: 51.6, cam: (t, k) => ({pos: lerp3([0, 6.4, 14], [-0.4, 6, 13], k), target: [-1, 4.6, 3], fov: 42})},
	{from: 51.6, to: 53.4, cam: (t, k) => ({pos: lerp3([-1.6, 3.4, 8], [-1.8, 3.3, 7.4], k), target: [PIG_M[0], 2.8, PIG_M[2]], fov: 40})},
	{from: 53.4, to: 55.0, cam: () => ({pos: [-1, 5.2, 10.5], target: [REQ_M[0], 4.3, REQ_M[2]], fov: 40})},
	{from: 55.0, to: JACKPOT, cam: (t, k) => ({pos: lerp3([-9, 4, 8], [-8.4, 4, 7.4], k), target: [-1.4, 3.2, 3], fov: 42})},
	{from: JACKPOT, to: 63.6, cam: (t, k) => ({pos: lerp3([0, 12, 26], [0, 13, 30], k), target: [0, 7, 3], fov: 54})},
	// broke
	{from: 74.0, to: 77.4, cam: () => ({pos: [0, 8.6, 12.5], target: [0, 8.6, 2], fov: 34})},
	{from: 77.4, to: 79, cam: (t, k) => ({pos: lerp3([3.4, 5.2, 11.6], [3.2, 5.1, 11.0], k), target: [REQ_M[0], 4.3, REQ_M[2]], fov: 40})},
];

export const MachineScene: React.FC<{t0: number; mode: 'win' | 'broke'}> = ({t0, mode}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const cam = withShake(shotAt(MACHINE_SHOTS, t).cam, t, t > JACKPOT && t < JACKPOT + 0.8 ? 0.12 : 0);
	const won = mode === 'win' && t > JACKPOT;
	// symbols: 0 cat, 1 diamond, 2 seven, 3 dog, 4 skull, 5 clover
	const spin: [number, number, number] =
		mode === 'broke'
			? [reel(t, 0, SPIN2 - 1.4, [], 4), reel(t, 1, SPIN2 - 1.4, [], 4), reel(t, 2, SPIN2 - 1.4, [], 4)]
			: t < JACKPOT
				? [reel(t, 0, SPIN1, [], 5), reel(t, 1, SPIN1, [], 0), reel(t, 2, SPIN1, [], 3)]
				: [2 + Math.max(0, JACKPOT + 0.6 - t) * 12, 2 + Math.max(0, JACKPOT + 0.4 - t) * 12, 2 + Math.max(0, JACKPOT + 0.2 - t) * 12];
	const pigIn = ease(range(t, WIN_PIGEON, WIN_PIGEON + 0.5));
	const pigP: V3 = mode === 'broke' ? PIG_M : lerp3([0, 4.6, 2.4], PIG_M, pigIn);
	const peck = t > PECK - 0.3 && t < PECK + 0.3 ? Math.sin(((t - PECK + 0.3) / 0.6) * Math.PI) * 0.8 : 0;
	const rf: Look['face'] = mode === 'broke' ? (t > 77.4 ? 'happy' : 'sad') : won ? 'grin' : t > WIN_PIGEON ? 'worried' : 'grin';
	const items: BB[] = [
		{p: REQ_M, name: 'REQ', talking: talking('req', t)},
	];
	if (t > WIN_PIGEON || mode === 'broke') items.push({p: [pigP[0], pigP[1] - 0.2, pigP[2]], h: 2.2, name: 'THE PIGEON', talking: talking('pigeon', t)});
	const dia = won ? Math.min(1e9, Math.pow(10, Math.min(9, (t - JACKPOT) * 4))) : 0;
	return (
		<AbsoluteFill>
			<Stage cam={cam} env={{...CASINO, shadowCenter: [0, 0, 6], shadowSize: 30}}>
				<Machine t={t} spin={spin} lights={won ? 1.7 : 1} />
				<Avatar look={REQ(rf)} position={REQ_M} rotationY={t > 53.4 && t < 55 ? face(REQ_M, [-1, 0, 10.5]) : mode === 'broke' && t > 77.4 ? 0.2 : Math.PI} pose={{time: t, point: (t > SPIN1 - 0.3 && t < SPIN1 + 0.8) || (mode === 'broke' && t < SPIN2 + 0.6) ? 1 : 0, armsUp: won ? 1 : 0, jump: won ? Math.abs(Math.sin(t * 8)) * 0.8 : 0}} />
				{t > WIN_PIGEON || mode === 'broke' ? (
					<group position={pigP} rotation={[peck, 0.4, 0]}>
						<Pigeon position={[0, 0, 0]} t={t} flap={won || pigIn < 1 ? 1 : 0} scale={1.4} />
					</group>
				) : null}
				{won ? (
					<>
						<CashRain t={t - JACKPOT} center={[0, 0, 6]} count={80} area={18} />
						{new Array(12).fill(0).map((_, i) => {
							const y = 18 - ((t - JACKPOT) * 6 + i * 1.7) % 18;
							return <Diamond key={i} position={[-8 + (i % 6) * 3.2, y, 4 + Math.floor(i / 6) * 4]} t={t + i} scale={0.6} />;
						})}
					</>
				) : null}
				<Spotlight position={[0, 20, 16]} target={[0, 2, 8]} intensity={700} color="#ffd9f2" />
			</Stage>
			<Billboards cam={cam} t={t} items={items} />
			<GameUI t={t} talking={talking('req', t)} mode="plain" chatFrom={45.6} />
			<Diamonds value={dia} t={t} flash={won} />
			{mode === 'win' ? (
				<>
					<BigText t={t} from={WIN_PIGEON + 0.2} to={51.4} text="YOU WON: 1 PIGEON 🕊️" color="#ffffff" top={150} size={90} />
					<BigText t={t} from={PECK} to={PECK + 0.7} text="*peck*" color="#ffd28a" top={440} size={80} />
					<BigText t={t} from={JACKPOT + 0.1} to={60.0} text="7 7 7 JACKPOT!!!" color="#ffd23f" top={150} size={120} />
					<PopWords t={t} until={63.2} words={[{at: 60.6, text: '99%', color: '#ffd23f', x: 1280, y: 300, rot: -8}, {at: 61.8, text: 'BIG WIN', color: '#7df9ff', x: 1360, y: 460, rot: 6}]} />
					<Flash t={t} at={JACKPOT} dur={0.5} color="#fff3b0" />
				</>
			) : (
				<BigText t={t} from={75.9} to={77.4} text="💀 💀 💀" color="#fff" top={150} size={110} />
			)}
			<Fade t={t} inAt={t0} inDur={0.05} outFrom={mode === 'broke' ? 78.5 : 999} outTo={mode === 'broke' ? 79 : 1000} />
		</AbsoluteFill>
	);
};

// ================================================================ rich for 11 seconds
const MANSION: V3 = [0, 0, -24];
const CAR: V3 = [9, 0, 2];
const REQ_R: V3 = [4, 0.05, 4];
const RICH_SHOTS: Shot[] = [
	{from: 63.6, to: 68.4, cam: (t, k) => ({pos: lerp3([26, 12, 36], [22, 10, 31], ease(k)), target: [0, 6, -10], fov: 50})},
	{from: 68.4, to: 71.0, cam: (t, k) => ({pos: lerp3([2.4, 5.2, 11.6], [2.6, 5.1, 11.0], k), target: [5.5, 4, 4], fov: 42})},
	{from: 71.0, to: 74.0, cam: (t, k) => ({pos: lerp3([22, 11, 34], [23, 12, 36], k), target: [0, 5, -8], fov: 52})},
];

export const RichScene: React.FC<{t0: number}> = ({t0}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const cam = withShake(shotAt(RICH_SHOTS, t).cam, t, t > POOF && t < POOF + 0.4 ? 0.1 : 0);
	const gone = t > POOF;
	const drain = range(t, 72.6, POOF);
	const dia = gone ? 0 : 1e9 * (1 - drain);
	const watch = Math.min(11, (t - 63.8) * (11 / (POOF - 63.8)));
	return (
		<AbsoluteFill>
			<Stage cam={cam} env={{...LOBBY_DAY, shadowCenter: [0, 0, -6], shadowSize: 50}}>
				<Grass />
				<Clouds t={t} />
				<Forest count={40} radius={[45, 140]} />
				{!gone ? (
					<>
						<GoldMansion position={MANSION} />
						<Car position={CAR} rotationY={-0.5} />
					</>
				) : (
					<Sparkles points={new Array(20).fill(0).map((_, i) => [(rand(i) - 0.5) * 30 + (i % 2 ? 0 : 9), 2 + rand(i + 3) * 12 + (t - POOF) * 3, (rand(i + 6) - 0.5) * 20 - 10] as V3)} t={t} color="#ffd23f" size={0.8} />
				)}
				<Avatar look={gone ? REQ('shock') : REQ_GOLD} position={REQ_R} rotationY={0.3} pose={{time: t, flex: !gone && t > 68.4 && t < 71 ? 1 : 0, armsUp: gone ? 1 : 0}} />
				{!gone ? <CashRain t={t - 63.6} center={[2, 0, 0]} count={70} area={26} /> : null}
			</Stage>
			<Billboards cam={cam} t={t} items={[{p: REQ_R, name: 'REQ', talking: talking('req', t)}]} />
			<GameUI t={t} talking={talking('req', t)} mode="plain" chatFrom={63.6} />
			<Diamonds value={dia} t={t} flash={drain > 0} />
			{t > 63.8 ? (
				<div style={{position: 'absolute', left: 0, right: 0, top: 150, textAlign: 'center'}}>
					<span style={{fontFamily: GAME_FONT, fontWeight: 700, fontSize: 90, color: watch >= 11 ? '#ff4d4d' : '#fff', WebkitTextStroke: '13px #121212', paintOrder: 'stroke fill'}}>⏱️ 0:{watch.toFixed(2).padStart(5, '0')}</span>
				</div>
			) : null}
			<BigText t={t} from={POOF + 0.1} to={74.0} text="POOF" color="#ffd23f" top={440} size={130} />
			<Fade t={t} inAt={t0} inDur={0.05} />
		</AbsoluteFill>
	);
};

// ================================================================ end card
export const EndCard2: React.FC<{t0: number}> = ({t0}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const lt = t - t0;
	const fadeOut = range(t, 84.4, 85);
	const soon = range(t, 80.7, 81.3);
	return (
		<AbsoluteFill style={{background: '#000'}}>
			{t < 85.2 ? (
				<AbsoluteFill style={{opacity: 1 - fadeOut}}>
					<div style={{position: 'absolute', left: 0, right: 0, top: 250, display: 'flex', justifyContent: 'center', gap: 40}}>
						{['R', 'E', 'Q', '2'].map((l, i) => {
							const k = ease(range(lt, 0.2 + i * 0.25, 0.6 + i * 0.25));
							return (
								<div key={l} style={{fontFamily: DOC_FONT, fontSize: 320, lineHeight: 1, color: i === 3 ? '#ff5b5b' : '#fff', opacity: k, transform: `translateY(${(1 - k) * -80}px) scale(${1.3 - 0.3 * k})`, marginLeft: i === 3 ? 50 : 0}}>
									{l}
								</div>
							);
						})}
					</div>
					<div style={{position: 'absolute', left: '50%', top: 590, width: 620 * ease(range(lt, 1.2, 1.8)), height: 5, background: '#ff5b5b', transform: 'translateX(-50%)'}} />
					<div style={{position: 'absolute', left: 0, right: 0, top: 700, textAlign: 'center', fontFamily: DOC_FONT, fontSize: 110, letterSpacing: 18, color: '#ffd6d0', opacity: soon}}>PART 3 COMING SOON</div>
				</AbsoluteFill>
			) : null}
			<Grain t={t} opacity={0.06} />
			<Letterbox />
		</AbsoluteFill>
	);
};
