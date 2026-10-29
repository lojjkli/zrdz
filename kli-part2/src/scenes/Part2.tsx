import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {Avatar, KLI_DEEP, KLI_RICH, MYNINN_LOOK, NOOB_KLI, npcLook} from '../three/Avatar';
import {Cam, ease, lerp, lerp3, range, V3} from '../three/cam';
import {Sparkles, Spotlight} from '../three/Props';
import {Clouds, Env, lerpEnv, Stage} from '../three/World';
import {Lobby, LOBBY_DAY, LOBBY_NIGHT, LOBBY_SUNSET} from '../three/MM2World';
import {Alley, baseplateTexture, Bread, CardboardBox, CashRain, DefaultCube, EnergyCan, Fork, GoldChair, GoldMansion, Pigeon, TalkingDonut, TeaTray, Throne, ViewportGrid} from '../three/KliProps';
import {rand} from '../three/textures';
import {bubbleOf, FPS, GIFT, HATERS, STAB, talking, ZAP} from '../timeline';
import {Billboards, BB} from '../ui/Billboards';
import {DOC_FONT, UI_FONT} from '../ui/HUD';
import {BigText, GameUI} from '../ui/MM2';
import {BlenderUI, Fade, Flash, PopWords, RobuxCounter} from '../ui/KliUI';
import {Grain, Letterbox, Vignette} from './Doc';
import {face, Shot, shotAt, withShake} from './shots';

export const VOID: Env = {
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

const MORNING: Env = {
	skyTop: '#5b7fd6',
	skyHorizon: '#ffc79a',
	sunDir: [0.6, 0.35, 0.7],
	sunColor: '#ffd2a1',
	sunIntensity: 2.3,
	hemiSky: '#ffe2c8',
	hemiGround: '#4a4048',
	hemiIntensity: 0.9,
	fog: ['#f2c6a8', 60, 260],
	sunGlow: 1.2,
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

const Y = 0.4;

// ================================================================ cold open
export const ColdOpen2: React.FC = () => {
	const t = useCurrentFrame() / FPS;
	const k = ease(range(t, 0, 9));
	const cam: Cam = withShake({pos: lerp3([0.4, 5.2, 9], [3.5, 4.8, 15], k), target: lerp3([-1, 4.9, 0], [-2.6, 4.4, 0], k), fov: 42}, t, t > 2.6 && t < 4.2 ? 0.05 : 0);
	const rise = ease(range(t, 2.6, 4.4));
	const prev = interpolate(t, [0.4, 0.8, 4.4, 4.8], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	const title = range(t, 5.2, 5.7);
	const sub = range(t, 6.0, 6.6);
	const out = range(t, 8.5, 9);
	return (
		<AbsoluteFill style={{background: '#000'}}>
			<Stage cam={cam} env={VOID}>
				<mesh position={[0, -0.25, 0]} receiveShadow>
					<cylinderGeometry args={[4, 4.3, 0.5, 48]} />
					<meshStandardMaterial color="#1f1f2c" roughness={0.3} metalness={0.4} />
				</mesh>
				<Spotlight position={[0, 22, 3]} target={[0, 0, 0]} intensity={1600} color="#e6e6ff" />
				<pointLight position={[2, 5, 7]} color="#e0dcff" intensity={30} distance={16} />
				<pointLight position={[0, 8, -10]} color="#ff4f8a" intensity={220 * rise} distance={30} />
				<Avatar look={KLI_DEEP} position={[0, 0, 0]} rotationY={0.25} pose={{time: t, headYaw: t > 3 ? 0.5 : 0}} />
				<TalkingDonut position={[0, lerp(-24, -3, rise), -12]} scale={4} t={t} mood="smug" />
			</Stage>
			<Vignette />
			<div style={{position: 'absolute', left: 120, top: 90, fontFamily: DOC_FONT, fontSize: 90, letterSpacing: 16, color: '#d8d8ff', opacity: prev}}>PREVIOUSLY...</div>
			<div style={{position: 'absolute', left: 150, top: 330, opacity: title, transform: `translateX(${(1 - title) * -40}px)`}}>
				<div style={{fontFamily: DOC_FONT, fontSize: 300, color: '#fff', letterSpacing: 40, lineHeight: 1}}>KLI 2</div>
				<div style={{height: 4, width: 640 * title, background: '#ff7fb6', marginTop: 10}} />
				<div style={{fontFamily: UI_FONT, fontSize: 40, color: '#d8d8d8', marginTop: 24, letterSpacing: 10, opacity: sub, fontWeight: 600}}>THE DONUT RETURNS</div>
			</div>
			<Grain t={t} />
			<Letterbox h={110 * (1 - out)} />
			<AbsoluteFill style={{background: '#000', opacity: Math.max(1 - t / 0.7, out)}} />
		</AbsoluteFill>
	);
};

// ================================================================ back in the box
const M_FROM: V3 = [14, 0, 8];
const M_TO: V3 = [3.6, 0, 6.5];
const BOX_SHOTS: Shot[] = [
	{from: 9, to: 13.2, cam: (t, k) => ({pos: lerp3([9, 12, 20], [5, 6.5, 13], ease(k)), target: [0, 2.5, 0], fov: 46})},
	{from: 13.2, to: 16, cam: (t, k) => ({pos: lerp3([0.6, 4.3, 6.4], [0.5, 4.2, 5.8], k), target: [0, 3.9, 0], fov: 40})},
	{from: 16, to: 18.6, cam: (t, k) => ({pos: lerp3([7.8, 6.2, 9.0], [7.2, 6.0, 8.4], k), target: [0, 3.2, 0], fov: 40})},
	{from: 18.6, to: 20.4, cam: (t) => ({pos: lerp3([0.6, 4.3, 6.4], [0.3, 4.0, 4.2], ease(range(t, 18.6, 18.9))), target: [0, 3.9, 0], fov: 40})},
	{from: 20.4, to: 24, cam: (t, k) => ({pos: lerp3([3, 6, 12], [6, 14, 20], ease(k)), target: [1, 2.5, 2], fov: 46})},
];

export const BoxScene: React.FC<{t0: number}> = ({t0}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const cam = shotAt(BOX_SHOTS, t).cam;
	const my = lerp3(M_FROM, M_TO, range(t, 14.0, 16.0));
	const myWalk = t > 14 && t < 16;
	const kTalk = talking('kli', t);
	return (
		<AbsoluteFill>
			<Stage cam={cam} env={{...MORNING, shadowCenter: [0, 0, 2], shadowSize: 22}}>
				<Alley wet={0.5} />
				<CardboardBox position={[0, 0, 0]} />
				<Avatar look={{...KLI_DEEP, face: t > 18.6 ? 'klishock' : 'klisad'}} position={[0, 0, -0.2]} rotationY={t > 16 ? 0.45 : 0} pose={{time: t, sit: 1, armsUp: t > 13.2 && t < 15.3 ? 0.5 : 0}} />
				<Avatar look={MYNINN_LOOK} position={my} rotationY={face(my, [0, 0, 0])} pose={{time: t + 2, walk: t * 9, walkAmt: myWalk ? 1 : 0, point: t > 16 && t < 18 ? 1 : 0}} />
			</Stage>
			<Billboards
				cam={cam}
				t={t}
				items={[
					{p: [0, -0.7, -0.2], name: 'lojjkli', talking: kTalk},
					{p: my, name: 'myninn', talking: talking('myninn', t)},
				]}
			/>
			<GameUI t={t} talking={kTalk} mode="plain" chatFrom={999} />
			<RobuxCounter value={0} pulse={t > 13.4 && t < 14.4 ? Math.abs(Math.sin(t * 20)) : 0} />
			<BigText t={t} from={13.4} to={15.4} text="ROBUX: 0 😐" color="#ff6b6b" top={470} size={100} />
			<Fade t={t} inAt={t0} inDur={0.5} outFrom={23.4} outTo={24} />
		</AbsoluteFill>
	);
};

// ================================================================ the donut on its throne (+ final battle)
const THRONE_AT: V3 = [0, Y, -10];
const DONUT_AT: V3 = [0, Y + 3.33, -9.6];
const DONUT_S = 2.4;
const DONUT_MOUTH: V3 = [0, DONUT_AT[1] + 0.55 * DONUT_S, DONUT_AT[2] + 1.2 * DONUT_S];
const BOWERS: {p: V3; i: number; name: string}[] = [
	{p: [-6, Y, 0], i: 3, name: HATERS[0].name},
	{p: [-2.2, Y, 1.2], i: 8, name: HATERS[1].name},
	{p: [2.2, Y, 1.2], i: 10, name: HATERS[2].name},
	{p: [6, Y, 0], i: 5, name: HATERS[3].name},
];
const KLI_THRONE: V3 = [0, Y, 7];

const THRONE_SHOTS: Shot[] = [
	{from: 24, to: 28.4, cam: (t, k) => ({pos: lerp3([7, 3, 18], [6, 6, 20], ease(k)), target: lerp3([0, 2, -9], [0, 8, -10], ease(k)), fov: 50})},
	{from: 28.4, to: 30.4, cam: (t, k) => ({pos: lerp3([16, 7, 4], [15, 7.5, 5], k), target: [0, 3, -3], fov: 50})},
	{from: 30.4, to: 34.6, cam: (t, k) => ({pos: lerp3([1.6, 6.2, -0.4], [1.3, 6.4, -1.4], k), target: [0, 7.6, -9.6], fov: 46})},
	{from: 34.6, to: ZAP, cam: (t, k) => ({pos: lerp3([4.5, 9.5, 15], [3.5, 9.0, 12.5], ease(k)), target: [0, 6.5, -9], fov: 46})},
	{from: ZAP, to: 40.9, cam: (t, k) => ({pos: [15, 7, 0], target: [0, 5, -1.5], fov: 52})},
	{from: 40.9, to: 46, cam: (t, k) => ({pos: lerp3([0.8, 5.2, 2.2], [0.6, 5.0, 3.0], k), target: [0, 4.8, KLI_THRONE[2]], fov: 44})},
];

const kliRun = (t: number): V3 => lerp3([0, Y, 14], [0, Y, -1], range(t, 73.2, 75.2));
const kliBattle = (t: number): V3 => {
	if (t < STAB) return kliRun(t);
	if (t < 82.0) return lerp3([0, Y, -1], [0, Y, 2], range(t, 76.4, 77.4));
	return lerp3([0, Y, 2], [0, Y, -3.4], range(t, 82.0, 83.0));
};
const FORK_STUCK: V3 = [-1.5, Y + 3.85, -3];

const BATTLE_SHOTS: Shot[] = [
	{from: 66, to: 69.2, cam: (t, k) => ({pos: lerp3([18, 9, 22], [16, 9, 20], k), target: [0, 5, -4], fov: 50})},
	{from: 69.2, to: 73.0, cam: (t, k) => ({pos: lerp3([1.6, 6.2, -0.4], [1.3, 6.4, -1.4], k), target: [0, 7.6, -9.6], fov: 46})},
	{from: 73.0, to: STAB, cam: (t) => {
		const p = kliRun(t);
		return {pos: [10, 5.5, p[2] + 4], target: [0, 4, p[2] - 3], fov: 50};
	}},
	{from: STAB, to: 78.4, cam: (t, k) => ({pos: lerp3([17, 8, -1], [16, 8.5, 0], k), target: [0, 6, -6], fov: 50})},
	{from: 78.4, to: 81.8, cam: (t, k) => ({pos: lerp3([2.2, 7.0, -1.6], [1.8, 7.2, -2.4], k), target: [0, 7.6, -9.6], fov: 46})},
	{from: 81.8, to: 87.4, cam: (t, k) => ({pos: lerp3([10, 7, 7], [9, 7.5, 6], k), target: [0, 5, -5], fov: 48})},
	{from: 87.4, to: GIFT, cam: (t, k) => ({pos: lerp3([11, 6, 3], [10, 6, 2], k), target: [0, 5, -4], fov: 48})},
	{from: GIFT, to: 94, cam: (t, k) => ({pos: lerp3([1.8, 2.0, 3.2], [1.5, 2.2, 2.6], k), target: [0, 5.6, -3.4], fov: 56})},
];

export const DonutScene: React.FC<{t0: number; mode: 'throne' | 'battle'}> = ({t0, mode}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const throne = mode === 'throne';
	const shake = throne ? (t > ZAP && t < ZAP + 0.6 ? 0.14 : 0) : (t > STAB && t < STAB + 0.6 ? 0.18 : 0) + (t > GIFT && t < GIFT + 0.5 ? 0.12 : 0);
	const cam = withShake(shotAt(throne ? THRONE_SHOTS : BATTLE_SHOTS, t).cam, t, shake);
	const env = throne ? {...LOBBY_DAY, shadowCenter: [0, 0, -2] as V3, shadowSize: 26} : {...LOBBY_SUNSET, shadowCenter: [0, 0, -2] as V3, shadowSize: 26};
	const dTalk = talking('donut', t);
	const kTalk = talking('kli', t);
	// kli
	const kp = throne ? KLI_THRONE : kliBattle(t);
	const deep = throne ? t < ZAP : t >= GIFT;
	const kFace = throne ? (t < ZAP ? 'kli' : t < 40 ? 'shock' : 'worried') : t < STAB ? 'grin' : t < 81.8 ? 'worried' : 'happy';
	const hug = !throne && t > 83.0 && t < 87.4;
	const holding = !throne && t < STAB;
	const running = !throne && t > 73.2 && t < STAB;
	// donut
	const mood = throne ? 'smug' : t < STAB ? 'smug' : t < 83.6 ? 'hurt' : 'happy';
	const tears = !throne && t > 78.2 && t < 84 ? 1 : 0;
	const wob = !throne && t > STAB && t < 78.2 ? 1 : 0;
	// voice orb: kli -> donut (throne), donut -> kli (battle)
	const orbK = throne ? range(t, ZAP + 0.1, ZAP + 1.2) : range(t, 88.6, GIFT);
	const orbOn = throne ? t > ZAP && t < ZAP + 1.2 : t > 88.6 && t < GIFT;
	const kHead: V3 = [kp[0], kp[1] + 4.6, kp[2]];
	const orbP = throne ? lerp3(kHead, DONUT_MOUTH, ease(orbK)) : lerp3(DONUT_MOUTH, kHead, ease(orbK));
	const bow = throne ? (t < 30.4 ? 0.7 : 0.25) : 0;
	const bbs: BB[] = [
		{p: kp, name: 'lojjkli', talking: kTalk, hearts: hug ? (t - 83.0) % 2.5 : undefined, emote: null},
		{p: DONUT_AT, h: 3.0 * DONUT_S + 1.2, name: 'TheDonut 👑', talking: dTalk},
	];
	if (throne) BOWERS.forEach((b) => bbs.push({p: b.p, name: b.name, bubble: bubbleOf(b.name, t)}));
	return (
		<AbsoluteFill>
			<Stage cam={cam} env={env}>
				<Lobby t={t} lampsOn={throne ? 0 : 0.6} />
				<Clouds t={t} />
				<Throne position={THRONE_AT} scale={1.6} />
				<TalkingDonut position={DONUT_AT} scale={DONUT_S} t={t} talk={dTalk} mood={mood} crown={throne || t < STAB} tears={tears} wobble={wob} />
				<pointLight position={[0, 9, -2]} color={throne ? '#ffd2a0' : '#ffb07a'} intensity={60} distance={22} decay={1.4} />
				<Avatar
					look={deep ? KLI_DEEP : {...NOOB_KLI, face: kFace as never}}
					position={kp}
					rotationY={!throne && t >= GIFT ? 0 : Math.PI}
					pose={{time: t, walk: t * 12, walkAmt: running ? 1 : 0, point: holding ? 1 : 0, armsUp: hug ? 0.55 : throne && t > ZAP && t < 40.6 ? 1 : 0, lean: running ? 0.25 : 0}}
				/>
				{throne
					? BOWERS.map((b, j) => (
							<Avatar
								key={b.i}
								look={{...npcLook(b.i), face: t > 41.4 && t < 43.2 ? 'grin' : 'happy'}}
								position={b.p}
								rotationY={t > 40.9 ? face(b.p, KLI_THRONE) : Math.PI}
								pose={{time: t + j, lean: t > 40.9 ? 0 : bow, armsUp: t > 28.6 && t < 30.2 ? 0.8 : 0, jump: t > 41.4 && t < 43 ? Math.abs(Math.sin((t + j) * 8)) * 0.6 : 0}}
							/>
					  ))
					: null}
				{holding ? <Fork position={[kp[0] - 1.5, kp[1] + 3.85, kp[2] - 2.0]} rotation={[0, Math.PI, 0]} scale={1.3} /> : null}
				{!throne && t >= STAB ? <Fork position={FORK_STUCK} rotation={[0.08, Math.PI, 0]} scale={1.3} /> : null}
				{orbOn ? (
					<group position={orbP}>
						<mesh>
							<sphereGeometry args={[0.6, 20, 14]} />
							<meshBasicMaterial color="#b49cff" />
						</mesh>
						<pointLight color="#b49cff" intensity={60} distance={10} />
					</group>
				) : null}
				{throne && t > ZAP - 0.05 && t < ZAP + 0.35 ? (
					<mesh position={lerp3(DONUT_MOUTH, kHead, 0.5)} rotation={[Math.atan2(DONUT_MOUTH[1] - kHead[1], kHead[2] - DONUT_MOUTH[2]) - Math.PI / 2, 0, 0]}>
						<cylinderGeometry args={[0.18, 0.18, Math.hypot(kHead[2] - DONUT_MOUTH[2], kHead[1] - DONUT_MOUTH[1]), 8]} />
						<meshBasicMaterial color="#e0d4ff" />
					</mesh>
				) : null}
				{!throne && t > STAB && t < STAB + 1.6 ? (
					<Sparkles
						points={new Array(30).fill(0).map((_, i) => {
							const e = t - STAB;
							return [(rand(i) - 0.5) * 14 * e, DONUT_AT[1] + 3 + (rand(i + 1) * 10 - 2) * e - 6 * e * e, -8 + (rand(i + 2) - 0.2) * 10 * e] as V3;
						})}
						t={t}
						color={['#ffd23f', '#3fc1ff', '#7cff6b', '#ff5a8a'][0]}
						size={0.25}
					/>
				) : null}
			</Stage>
			<Billboards cam={cam} t={t} items={bbs} />
			<GameUI t={t} talking={kTalk} mode="plain" chatFrom={throne ? 24 : 66} />
			{throne ? (
				<>
					<BigText t={t} from={25.4} to={28.3} text="👑 CEO OF ROBLOX 👑" color="#ffd84d" top={470} size={96} />
					<BigText t={t} from={35.4} to={38.1} text="RULE #1: NO DEEP VOICES" color="#ff6b6b" top={470} size={84} />
					<Flash t={t} at={ZAP} dur={0.4} color="#e0d4ff" />
					<BigText t={t} from={39.7} to={41.2} text="VOICE: STOLEN 🐭" color="#ff9ad5" top={470} size={96} />
				</>
			) : (
				<>
					<BigText t={t} from={66.8} to={68.9} text="⚔️ FINAL BATTLE ⚔️" color="#ff8a3d" top={470} size={100} />
					<BigText t={t} from={STAB} to={STAB + 1.4} text="CRITICAL HIT 🍴" color="#ffd84d" top={470} size={110} />
					<Flash t={t} at={STAB} dur={0.3} />
					<Flash t={t} at={GIFT} dur={0.6} color="#e0d4ff" />
					<BigText t={t} from={GIFT + 0.3} to={GIFT + 2.2} text="VOICE: RESTORED 🔊" color="#c8b8ff" top={470} size={96} />
				</>
			)}
			<Fade t={t} inAt={t0} inDur={0.5} outFrom={throne ? 45.4 : 93.4} outTo={throne ? 46 : 94} />
		</AbsoluteFill>
	);
};

// ================================================================ the plan (night)
const K_PLAN: V3 = [-1.4, Y, 14];
const M_PLAN: V3 = [1.6, Y, 14.6];
const PLAN_SHOTS: Shot[] = [
	{from: 46, to: 49.2, cam: (t, k) => ({pos: lerp3([8, 7, 26], [6, 6.5, 24], k), target: [0, 3.5, 14], fov: 46})},
	{from: 49.2, to: 51.4, cam: (t, k) => ({pos: [M_PLAN[0] - 2.6, 5.2, M_PLAN[2] + 4.2], target: [M_PLAN[0], 4.6, M_PLAN[2]], fov: 42})},
	{from: 51.4, to: 54, cam: (t, k) => ({pos: lerp3([K_PLAN[0] + 2.4, 5.0, K_PLAN[2] + 4.4], [K_PLAN[0] + 1.8, 4.9, K_PLAN[2] + 3.6], ease(range(t, 51.4, 51.7))), target: [K_PLAN[0], 4.6, K_PLAN[2]], fov: 42})},
];

export const PlanScene: React.FC<{t0: number}> = ({t0}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const cam = shotAt(PLAN_SHOTS, t).cam;
	const kTalk = talking('kli', t);
	return (
		<AbsoluteFill>
			<Stage cam={cam} env={{...LOBBY_NIGHT, shadowCenter: [0, 0, 14], shadowSize: 20}}>
				<Lobby t={t} lampsOn={1} />
				<pointLight position={[0, 6, 18]} color="#c8d6ff" intensity={40} distance={14} />
				<Avatar look={{...NOOB_KLI, face: t > 51.6 ? 'happy' : 'sad'}} position={K_PLAN} rotationY={face(K_PLAN, M_PLAN)} pose={{time: t, jump: t > 51.7 && t < 52.4 ? Math.sin(((t - 51.7) / 0.7) * Math.PI) * 1.6 : 0, armsUp: t > 51.7 && t < 52.4 ? 1 : 0}} />
				<Avatar look={MYNINN_LOOK} position={M_PLAN} rotationY={face(M_PLAN, K_PLAN)} pose={{time: t + 1}} />
			</Stage>
			<Billboards
				cam={cam}
				t={t}
				items={[
					{p: K_PLAN, name: 'lojjkli', talking: kTalk, emote: {char: '💡', age: t - 51.6}},
					{p: M_PLAN, name: 'myninn', talking: talking('myninn', t)},
				]}
			/>
			<GameUI t={t} talking={kTalk} mode="plain" chatFrom={999} />
			<BigText t={t} from={51.7} to={53.6} text="🍴 A FORK!" color="#e8eef5" top={470} size={120} />
			<Fade t={t} inAt={t0} inDur={0.5} outFrom={53.5} outTo={54} />
		</AbsoluteFill>
	);
};

// ================================================================ building the fork
export const ForgeScene: React.FC<{t0: number}> = ({t0}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const cam: Cam = {pos: lerp3([14, 8.5, 14], [12, 7.5, 12], range(t, 54, 66)), target: [0, 4.4, 0], fov: 44};
	const grow = ease(range(t, 56.0, 58.4));
	const cans = Math.floor(Math.max(0, Math.min(8, (t - 60.0) / 0.4 + 1)));
	const shine = t > 64 ? 1 : 0;
	return (
		<AbsoluteFill style={{background: '#3d3d3d'}}>
			<Stage cam={cam} env={VIEWPORT}>
				<ViewportGrid />
				<DefaultCube scale={t < 55.4 ? 1 : 0} />
				{grow > 0 ? (
					<group rotation={[0, t * 0.8, 0]}>
						<Fork position={[0, 0.3, 0]} rotation={[-Math.PI / 2, 0, 0]} scale={1.25 * grow} shine={shine} />
					</group>
				) : null}
				{new Array(cans).fill(0).map((_, i) => {
					const a = (i / 8) * Math.PI * 2;
					return <EnergyCan key={i} position={[Math.cos(a) * 3.6, 0.6, Math.sin(a) * 3.6]} rotation={[0, 0, i % 3 === 0 ? Math.PI / 2 : 0]} />;
				})}
				{shine ? <Sparkles points={new Array(14).fill(0).map((_, i) => [Math.sin(i * 1.9) * 1.6, 1 + i * 0.6, Math.cos(i * 1.9) * 1.6] as V3)} t={t} color="#ffffff" size={0.2} /> : null}
			</Stage>
			<BlenderUI t={t} outliner={t < 55.4 ? ['Camera', 'Light', 'Cube'] : t < 56 ? ['Camera', 'Light'] : ['Camera', 'Light', 'THE_FORK']} title="FORK_final_v67.blend" />
			<PopWords
				t={t}
				until={63.6}
				words={[
					{at: 59.6, text: '⏰ 40 HOURS', x: 600, y: 380, rot: -5, color: '#ffd84d'},
					{at: 61.6, text: '🥤 x30', x: 1150, y: 600, rot: 4, color: '#7cff3a'},
				]}
			/>
			<BigText t={t} from={64.0} to={65.6} text="IT'S BEAUTIFUL 😭" color="#ffffff" top={470} size={100} />
			<Fade t={t} inAt={t0} inDur={0.4} outFrom={65.5} outTo={66} />
		</AbsoluteFill>
	);
};

// ================================================================ the donut is a butler now
const Grass: React.FC = () => (
	<mesh position={[0, -0.5, 0]} receiveShadow>
		<boxGeometry args={[400, 1, 400]} />
		<meshStandardMaterial map={baseplateTexture('richgrass', '#4f9a3a', '#468a33', 100)} roughness={0.9} />
	</mesh>
);
const B_DONUT_FROM: V3 = [14, 0, 6];
const B_DONUT_TO: V3 = [3.2, 0, 2.2];
const MY_B: V3 = [-4.2, 0, 2.5];
const BUTLER_SHOTS: Shot[] = [
	{from: 94, to: 98.4, cam: (t, k) => ({pos: lerp3([12, 7, 17], [10, 6.5, 15], k), target: [0, 3, -1], fov: 48})},
	{from: 98.4, to: 100.6, cam: (t, k) => ({pos: [7.6, 3.6, 6.2], target: [B_DONUT_TO[0], 2.4, B_DONUT_TO[2]], fov: 44})},
	{from: 100.6, to: 102, cam: () => ({pos: [0.6, 4.4, 5.6], target: [0, 4.0, 0], fov: 42})},
	{from: 102, to: 106, cam: (t, k) => ({pos: lerp3([4, 6, 12], [10, 16, 24], ease(k)), target: [0, 4, -6], fov: 50})},
];

export const ButlerScene: React.FC<{t0: number}> = ({t0}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const cam = shotAt(BUTLER_SHOTS, t).cam;
	const dk = range(t, 95.0, 97.6);
	const hop = t > 95 && t < 97.6 ? Math.abs(Math.sin(t * 7)) * 0.6 : 0;
	const dp = lerp3(B_DONUT_FROM, B_DONUT_TO, dk);
	const dTalk = talking('donut', t);
	const kTalk = talking('kli', t);
	const dYaw = -0.35;
	return (
		<AbsoluteFill>
			<Stage cam={cam} env={{...LOBBY_DAY, shadowCenter: [0, 0, -4], shadowSize: 30}}>
				<Grass />
				<Clouds t={t} />
				<GoldMansion position={[0, 0, -32]} />
				<GoldChair position={[0, 0, 0]} />
				<Avatar look={KLI_RICH} position={[0, 0.25, 0.1]} pose={{time: t, sit: 1, wave: t > 100.6 && t < 101.8 ? 0.6 : 0}} />
				<TalkingDonut position={[dp[0], dp[1] + hop, dp[2]]} yaw={dYaw} scale={1.25} t={t} talk={dTalk} mood="happy" bowtie />
				<TeaTray position={[dp[0] - 0.6, 2.1 + hop, dp[2] + 1.2]} />
				<Avatar look={MYNINN_LOOK} position={MY_B} rotationY={face(MY_B, [0, 0, 6])} pose={{time: t + 2, wave: t > 99 && t < 100.4 ? 1 : 0}} />
				<CashRain t={t} center={[0, 0, -4]} area={40} count={90} />
			</Stage>
			<Billboards
				cam={cam}
				t={t}
				items={[
					{p: [0, -0.5, 0.1], name: 'lojjkli', talking: kTalk},
					{p: dp, h: 4.6, name: 'TheDonut', talking: dTalk, bubble: bubbleOf('TheDonut', t)},
					{p: MY_B, name: 'myninn', bubble: bubbleOf('myninn', t)},
				]}
			/>
			<GameUI t={t} talking={kTalk} mode="plain" chatFrom={98} />
			<RobuxCounter value={999_999_999} gold />
			<BigText t={t} from={95.2} to={97.6} text="🎩 BUTLER MODE" color="#ffffff" top={470} size={100} />
			<Fade t={t} inAt={t0} inDur={0.5} outFrom={105.4} outTo={106} />
		</AbsoluteFill>
	);
};

// ================================================================ end card + post-credit pigeon
export const EndCard2: React.FC<{t0: number}> = ({t0}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const lt = t - t0;
	const fadeOut = range(t, 111.6, 112.2);
	const by = range(t, 107.6, 108.2);
	const soon = range(t, 108.2, 108.8);
	const post = t > 112.6;
	const pt = t - 112.6;
	const cam: Cam = withShake({pos: lerp3([0, 5.0, 7.4], [0, 5.0, 6.0], ease(range(t, 112.6, 120))), target: [0, 4.9, 0], fov: 40}, t, t > 118.6 && t < 119.2 ? 0.05 : 0);
	const pk = range(t, 117.0, 118.4);
	const pigeon: V3 = lerp3([-9, 6.4, 1.6], [9, 6.0, 1.6], pk);
	return (
		<AbsoluteFill style={{background: '#000'}}>
			{!post ? (
				<AbsoluteFill style={{opacity: 1 - fadeOut}}>
					<div style={{position: 'absolute', left: 0, right: 0, top: 250, display: 'flex', justifyContent: 'center', gap: 40}}>
						{['K', 'L', 'I', '2'].map((l, i) => {
							const k = ease(range(lt, 0.2 + i * 0.25, 0.6 + i * 0.25));
							return (
								<div key={l} style={{fontFamily: DOC_FONT, fontSize: 320, lineHeight: 1, color: i === 3 ? '#ff8fc8' : '#fff', opacity: k, transform: `translateY(${(1 - k) * -80}px) scale(${1.3 - 0.3 * k})`, textShadow: '0 0 50px rgba(255,127,182,0.5)', marginLeft: i === 3 ? 50 : 0}}>
									{l}
								</div>
							);
						})}
					</div>
					<div style={{position: 'absolute', left: '50%', top: 590, width: 620 * ease(range(lt, 1.2, 1.8)), height: 5, background: '#ff8fc8', transform: 'translateX(-50%)'}} />
					<div style={{position: 'absolute', left: 0, right: 0, top: 620, textAlign: 'center', fontFamily: UI_FONT, fontSize: 38, letterSpacing: 14, color: '#cfcfcf', opacity: by, fontWeight: 600}}>A STORY BY LOJJKLI</div>
					<div style={{position: 'absolute', left: 0, right: 0, top: 700, textAlign: 'center', fontFamily: DOC_FONT, fontSize: 110, letterSpacing: 18, color: '#ffb3d6', opacity: soon, transform: `scale(${1.08 - 0.08 * soon})`}}>
						PART 3 COMING SOON
					</div>
				</AbsoluteFill>
			) : (
				<AbsoluteFill style={{opacity: interpolate(pt, [0, 0.3, 6.8, 7.4], [0, 1, 1, 0], {extrapolateRight: 'clamp'})}}>
					<Stage cam={cam} env={VOID}>
						<Spotlight position={[2, 10, 6]} target={[0, 4.5, 0]} intensity={700} color="#c9b8ff" />
						<pointLight position={[-3, 5, 4]} color="#7b5cff" intensity={30} distance={14} />
						<Avatar look={{...KLI_DEEP, face: t > 116.9 ? 'klishock' : 'kli'}} position={[0, 0, 0]} pose={{time: t, headYaw: t > 117.2 && t < 118.6 ? lerp(-0.6, 0.6, pk) : 0}} />
						{pk > 0 && pk < 1 ? (
							<group>
								<Pigeon position={pigeon} rotationY={Math.PI / 2} t={t} scale={1.0} />
								<Bread position={[pigeon[0], pigeon[1] - 0.45, pigeon[2]]} scale={0.5} />
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
