import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {ADE_LOOK, Avatar, KLI_MM2, LIA_LOOK, Look, MIKEY_LOOK, REQ_LOOK, YF_LOOK} from '../three/Avatar';
import {Cam, clamp01, ease, easeOut, lerp, lerp3, range, V3} from '../three/cam';
import {Sparkles} from '../three/Props';
import {Stage} from '../three/World';
import {Coin, INDOOR, Mansion} from '../three/MM2World';
import {bubbleOf, FPS, talking} from '../timeline';
import {Billboards} from '../ui/Billboards';
import {GAME_FONT, outlined} from '../ui/HUD';
import {BigText, GameUI} from '../ui/MM2';
import {face, Shot, shotAt, withShake} from './shots';

const KLI: V3 = [6, 0, -1.5];
const LIA_IN: V3 = [-9, 0, 11];
const LIA: V3 = [1, 0, 6.5];
const REQ: V3 = [-3, 0, 4.2];
const MIKEY: V3 = [5.2, 0, 8.8];
const ADE: V3 = [9.8, 0, 5.6];
const DOOR: V3 = [9, 0, -15.5];
const YF_STAND: V3 = [13.5, 0, -3.5];
const GROUP: V3 = [3, 0, 6.5];

const COINS: V3[] = [
	[-7, 0, 10.4],
	[-4.6, 0, 9.4],
	[-2.2, 0, 8.3],
	[11, 0, -10],
	[-12, 0, -8],
	[14, 0, 10],
	[-14, 0, 2],
];

const liaPos = (t: number): V3 => lerp3(LIA_IN, LIA, ease(range(t, 30.7, 33.2)));
const coinTaken = (c: V3, t: number) => {
	// taken when Lia walks past it
	for (let s = 30.7; s <= t; s += 0.1) {
		const p = liaPos(s);
		if (Math.hypot(p[0] - c[0], p[2] - c[2]) < 1.2) return true;
	}
	return false;
};

const yfPos = (t: number): V3 => {
	if (t < 67.6) return lerp3(DOOR, YF_STAND, ease(range(t, 57.0, 59.0)));
	return lerp3(YF_STAND, DOOR, ease(range(t, 67.6, 68.8)));
};

// friends disappear when they leave the game
const LEAVE: Record<string, number> = {Mikey: 69.8, Ade: 70.6, REQ: 71.2, lojjkli: 71.6};
const poof = (name: string, t: number) => 1 - clamp01((t - (LEAVE[name] ?? 999)) / 0.22);

const meter = (t: number) => clamp01((t - 50.8) / 2.2);

const SHOTS: Shot[] = [
	{from: 30.6, to: 32.9, cam: (t, k) => ({pos: lerp3([-13, 9.5, 13], [-11, 8.2, 11.5], ease(k)), target: [2, 3.2, 1], fov: 54})},
	{from: 32.9, to: 34.2, cam: (t, k) => ({pos: lerp3([3.0, 2.8, 5.6], [3.6, 3.0, 4.2], ease(k)), target: [KLI[0], 4.7, KLI[2]], fov: 40})},
	{from: 34.2, to: 38.0, cam: (t, k) => ({pos: lerp3([0.8, 6.0, 11.6], [1.2, 5.8, 10.8], k), target: [KLI[0], 4.3, KLI[2]], fov: 44})},
	{from: 38.0, to: 40.8, cam: (t, k) => ({pos: lerp3([15, 7, 13], [14, 6.4, 11.5], k), target: [3.5, 3.8, 3], fov: 50})},
	{from: 40.8, to: 43.6, cam: (t, k) => ({pos: lerp3([3.0, 5.0, 5.8], [4.6, 4.8, 2.0], ease(k)), target: [KLI[0], 4.6, KLI[2]], fov: 40})},
	{from: 43.6, to: 45.0, cam: (t) => ({pos: [4.85, 4.7, 1.25], target: [KLI[0], 4.62, KLI[2]], fov: lerp(36, 28, easeOut(range(t, 43.6, 43.75)))})},
	{from: 45.0, to: 46.4, cam: (t, k) => ({pos: lerp3([6.6, 6.0, -0.4], [6.4, 5.8, 0.2], k), target: [3, 4.2, 6.5], fov: 55})},
	{from: 46.4, to: 49.1, cam: (t, k) => ({pos: lerp3([3.4, 5.2, 4.4], [3.9, 5.1, 3.4], k), target: [KLI[0], 4.4, KLI[2]], fov: 44})},
	{from: 49.1, to: 50.6, cam: (t) => ({pos: [2.7, 4.9, 3.9], target: [LIA[0], 4.6, LIA[2]], fov: lerp(50, 30, easeOut(range(t, 49.35, 49.5)))})},
	{
		from: 50.6,
		to: 54.8,
		cam: (t, k) => {
			const a = lerp(-0.2, 1.1, k) + Math.atan2(GROUP[0] - KLI[0], GROUP[2] - KLI[2]);
			return {pos: [KLI[0] + Math.sin(a) * 6.5, lerp(4.2, 5.6, k), KLI[2] + Math.cos(a) * 6.5], target: [KLI[0], 4.2, KLI[2]], fov: 44};
		},
	},
	{from: 54.8, to: 59.0, cam: (t, k) => ({pos: lerp3([-6, 8, 12], [-5, 7.6, 10.5], k), target: [7, 3.8, -6], fov: 52})},
	{from: 59.0, to: 62.6, cam: (t, k) => ({pos: lerp3([9.6, 5.4, 2.4], [10.2, 5.3, 1.4], k), target: [YF_STAND[0], 4.5, YF_STAND[2]], fov: 42})},
	{from: 62.6, to: 64.0, cam: (t, k) => ({pos: lerp3([3.0, 4.9, 3.8], [2.7, 4.85, 4.2], k), target: [LIA[0], 4.55, LIA[2]], fov: 40})},
	{from: 64.0, to: 67.0, cam: (t, k) => ({pos: lerp3([-8, 7, 13], [-7, 6.6, 12], k), target: [5, 3.5, -2], fov: 52})},
	{from: 67.0, to: 69.0, cam: (t, k) => ({pos: lerp3([3.5, 6, 8.5], [4, 5.8, 7.5], k), target: [9, 4, -12], fov: 46})},
	{from: 69.0, to: 72.0, cam: (t, k) => ({pos: lerp3([-1.9, 7.2, 11.2], [-1.4, 6.6, 10.4], k), target: [4, 3.5, 0.5], fov: 50})},
];

export const MansionScene: React.FC<{t0: number}> = ({t0}) => {
	const frame = useCurrentFrame();
	const t = t0 + frame / FPS;
	const {cam: base} = shotAt(SHOTS, t);
	const kliTalk = talking('kli', t);
	const deep = t >= 43.6 && t < 45.0 ? 0.09 * (1 - (t - 43.6) / 1.4) : kliTalk ? 0.025 : 0;
	const cam: Cam = withShake(base, t, deep);
	const lia = liaPos(t);
	const walking = t > 30.7 && t < 33.2;
	const walkAmt = walking ? Math.min(1, (t - 30.7) * 4, (33.2 - t) * 4) : 0;
	const yf = yfPos(t);
	const yfIn = t >= 56.9 && t < 68.8;
	const yfWalk = (t > 57.0 && t < 59.0) || (t > 67.6 && t < 68.8);
	const yfYaw = t < 59.0 ? face(DOOR, YF_STAND) : t < 67.4 ? face(YF_STAND, GROUP) : face(YF_STAND, DOOR);
	const shocked = t >= 43.8 && t < 50.6;
	const liaFace: Look['face'] = t >= 61.8 ? 'liasad' : shocked ? 'liashock' : 'lia';
	const friendFace = (def: Look['face']): Look['face'] => (shocked ? 'shock' : t > 60 ? 'worried' : def);
	const liaTarget = t > 57.5 && t < 69 ? yf : KLI;
	const liaYaw = walking ? face(LIA_IN, LIA) : face(lia, liaTarget);
	const hop = t > 35.0 && t < 35.5 ? Math.sin(((t - 35.0) / 0.5) * Math.PI) * 1.2 : 0;
	const coins = COINS.filter((c) => coinTaken(c, t)).length;
	const kliPoint = range(t, 55.4, 55.8) * (1 - range(t, 57.6, 58.0));
	const kliYaw = t > 55.2 && t < 58.4 ? lerp(face(KLI, GROUP), face(KLI, DOOR), ease(range(t, 55.2, 55.7)) * (1 - ease(range(t, 58.0, 58.4)))) : face(KLI, GROUP);
	const yfPoint = range(t, 61.6, 61.9) * (1 - range(t, 63.6, 64.0)) + range(t, 64.6, 64.9) * (1 - range(t, 66.4, 66.8));
	const friends = [
		{look: {...REQ_LOOK, face: friendFace('smile')}, p: REQ, name: 'REQ'},
		{look: {...MIKEY_LOOK, face: friendFace('grin')}, p: MIKEY, name: 'Mikey'},
		{look: {...ADE_LOOK, face: friendFace('smile')}, p: ADE, name: 'Ade'},
	];
	const emote = (at: number, char: string) => (t >= at ? {char, age: t - at} : null);
	const emotes: Record<string, {char: string; age: number} | null> = {
		Mikey: t < 44 ? emote(35.0, '💅') : t < 60 ? emote(45.1, '💀') : emote(63.0, '😐'),
		Ade: t < 44 ? emote(36.2, '✨') : t < 60 ? emote(45.3, '😳') : emote(63.6, '😠'),
		REQ: t < 60 ? emote(45.5, '‼️') : null,
		lojjkli: emote(37.8, '😏'),
	};
	const sparkle = (name: string, p: V3): V3[] => {
		const at = LEAVE[name];
		if (t < at || t > at + 0.8) return [];
		const k = t - at;
		return new Array(10).fill(0).map((_, j) => [p[0] + Math.cos(j * 0.63) * k * 4, 3 + Math.sin(j * 1.7) * 2 + k * 2, p[2] + Math.sin(j * 0.63) * k * 4] as V3);
	};
	return (
		<AbsoluteFill>
			<Stage cam={cam} env={INDOOR}>
				<Mansion t={t} doorOpen={ease(range(t, 56.9, 57.3)) * (1 - ease(range(t, 68.6, 69.0)))} />
				{COINS.map((c, i) => (coinTaken(c, t) ? null : <Coin key={i} position={c} t={t} />))}
				<Avatar look={{...LIA_LOOK, face: liaFace}} position={lia} rotationY={liaYaw} pose={{walk: (t - 30.7) * 9, walkAmt, time: t, jump: hop, wave: t > 34.3 && t < 35.0 ? 1 : 0}} />
				{friends.map((f, i) =>
					poof(f.name, t) > 0 ? (
						<Avatar
							key={f.name}
							look={f.look}
							position={f.p}
							scale={poof(f.name, t)}
							rotationY={face(f.p, t > 57.5 && t < 69 ? yf : KLI)}
							pose={{time: t + i * 1.7, armsUp: shocked && t < 46.2 ? 0.5 : 0, jump: shocked && t < 45.6 ? Math.abs(Math.sin((t - 43.8) * 8)) * 0.5 : 0}}
						/>
					) : null,
				)}
				{poof('lojjkli', t) > 0 ? (
					<Avatar look={{...KLI_MM2, face: t > 49.3 && t < 50.6 ? 'kliwide' : 'kli'}} position={KLI} scale={poof('lojjkli', t)} rotationY={kliYaw} pose={{time: t, point: kliPoint}} />
				) : null}
				{yfIn ? <Avatar look={YF_LOOK} position={yf} rotationY={yfYaw} pose={{walk: t * 9, walkAmt: yfWalk ? 1 : 0, time: t, point: yfPoint}} /> : null}
				{Object.keys(LEAVE).map((n) => {
					const p = n === 'lojjkli' ? KLI : friends.find((f) => f.name === n)!.p;
					return <Sparkles key={n} points={sparkle(n, p)} t={t} color="#ffffff" size={0.3} />;
				})}
			</Stage>
			<Billboards
				cam={cam}
				t={t}
				items={[
					{p: lia, talking: talking('lia', t)},
					...friends
						.filter((f) => poof(f.name, t) > 0.5)
						.map((f) => ({p: f.p, name: f.name, talking: f.name === 'REQ' && talking('req', t), bubble: bubbleOf(f.name, t), emote: emotes[f.name]})),
					...(poof('lojjkli', t) > 0.5 ? [{p: KLI, name: 'lojjkli', talking: kliTalk, bubble: kliTalk ? null : bubbleOf('lojjkli', t), emote: t < 40 ? emotes.lojjkli : null}] : []),
					...(yfIn ? [{p: yf, name: 'YF', talking: talking('yf', t), bubble: talking('yf', t) ? null : bubbleOf('YF', t)}] : []),
				]}
			/>
			<GameUI t={t} talking={talking('lia', t)} mode="round" roundStart={30.6} coins={coins} stick={walking ? [0.5 * walkAmt, -walkAmt] : [0, 0]} jump={hop > 0} />
			{/* the e-boy voice meter */}
			{t >= 50.6 && t < 54.8 ? <VoiceMeter t={t} /> : null}
			<BigText t={t} from={49.4} to={50.5} text="WHAT?!" color="#ff8fd0" top={140} size={130} />
			{/* bass punch: brief flash + zoom on the first "wsg" */}
			<AbsoluteFill style={{background: '#000', opacity: t > 42.9 && t < 43.6 ? 0.35 : 0}} />
			<AbsoluteFill style={{background: '#fff', opacity: t >= 43.6 && t < 43.8 ? (1 - (t - 43.6) / 0.2) * 0.5 : 0}} />
			<AbsoluteFill style={{background: '#000', opacity: Math.max(1 - clamp01((t - t0) / 0.3), range(t, 71.6, 72.0))}} />
		</AbsoluteFill>
	);
};

const VoiceMeter: React.FC<{t: number}> = ({t}) => {
	const k = meter(t);
	const o = interpolate(t, [50.6, 50.9, 54.5, 54.8], [0, 1, 1, 0]);
	const over = k >= 1;
	const flash = over ? 0.6 + 0.4 * Math.sin(t * 20) : 1;
	return (
		<div style={{position: 'absolute', right: 160, top: 170, width: 150, height: 560, opacity: o}}>
			<div style={{...outlined, WebkitTextStroke: '6px #121212', fontSize: 30, textAlign: 'center', marginBottom: 10}}>VOICE DEPTH</div>
			<div style={{position: 'relative', width: 90, height: 460, margin: '0 auto', borderRadius: 18, background: 'rgba(0,0,0,0.55)', border: '5px solid #121212', overflow: 'hidden'}}>
				<div
					style={{
						position: 'absolute',
						left: 0,
						right: 0,
						bottom: 0,
						height: `${k * 100}%`,
						background: 'linear-gradient(0deg,#3cff5a,#ffe14d 55%,#ff3030)',
						opacity: flash,
					}}
				/>
				{[0.25, 0.5, 0.75].map((y) => (
					<div key={y} style={{position: 'absolute', left: 0, right: 0, bottom: `${y * 100}%`, height: 3, background: 'rgba(0,0,0,0.5)'}} />
				))}
			</div>
			{over ? (
				<div
					style={{
						position: 'absolute',
						left: -120,
						right: -120,
						top: 250,
						textAlign: 'center',
						fontFamily: GAME_FONT,
						fontWeight: 700,
						fontSize: 54,
						color: '#ff3030',
						WebkitTextStroke: '9px #1a0000',
						paintOrder: 'stroke fill',
						transform: `rotate(-12deg) scale(${1 + 0.06 * Math.sin(t * 20)})`,
						whiteSpace: 'nowrap',
					}}
				>
					⚠️ TOO DEEP ⚠️
				</div>
			) : null}
		</div>
	);
};
