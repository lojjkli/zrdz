import React, {useMemo} from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {ADE_LOOK, Avatar, BOOMP_LOOK, kidLook, KLI_MM2, LIA_LOOK, Look, MIKEY_LOOK, REQ_LOOK} from '../three/Avatar';
import {Cam, clamp01, ease, easeOut, lerp, lerp3, range, V3} from '../three/cam';
import {Petals, Rain, Sparkles} from '../three/Props';
import {Clouds, lerpEnv, Stage} from '../three/World';
import {DutchFlag, GasCloud, LightBeam, Lobby, LOBBY_NIGHT, LOBBY_SUNSET, StinkPuffs, TOXIC, Tulips, Windmill} from '../three/MM2World';
import {rand} from '../three/textures';
import {bubbleOf, FPS, KID_POP, talking} from '../timeline';
import {Billboards, BB} from '../ui/Billboards';
import {GAME_FONT, outlined, UI_FONT} from '../ui/HUD';
import {AlertBanner} from '../ui/Dialogs';
import {BigText, GameUI, NameCard} from '../ui/MM2';
import {face, Shot, shotAt, withShake} from './shots';

const Y = 0.4;
const BENCH: V3 = [0, Y, 20];
const LIA_SIT: V3 = [0, Y, 20.25];

// ================================================================ sad: alone in the rain
const SAD_SHOTS: Shot[] = [
	{from: 72, to: 76.3, cam: (t, k) => ({pos: lerp3([-16, 18, -6], [-12, 14, 2], ease(k)), target: [0, 2, 18], fov: 48})},
	{from: 76.3, to: 78.6, cam: (t, k) => ({pos: lerp3([1.3, 3.5, 15.2], [1.0, 3.45, 15.9], k), target: [0, 3.95, LIA_SIT[2]], fov: 42})},
	{from: 78.6, to: 84, cam: (t, k) => ({pos: lerp3([2, 6, 13], [6, 22, -8], ease(k)), target: [0, 2, 19], fov: 50})},
];

export const SadScene: React.FC<{t0: number}> = ({t0}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const {cam} = shotAt(SAD_SHOTS, t);
	const flash = t > 74.0 && t < 74.25 ? 1 - (t - 74.0) / 0.25 : 0;
	return (
		<AbsoluteFill>
			<Stage cam={cam} env={{...LOBBY_NIGHT, sunIntensity: LOBBY_NIGHT.sunIntensity + flash * 3, shadowCenter: [0, 0, 16], shadowSize: 30}}>
				<Lobby lampsOn={1} t={t} />
				<Clouds t={t} color="#2a3045" opacity={0.85} />
				<Rain t={t} center={[0, 0, 14]} area={70} count={1400} />
				<pointLight position={[1.5, 5.5, 16.5]} color="#9fb6ff" intensity={30} distance={10} decay={1.5} />
				<Avatar look={{...LIA_LOOK, face: 'liacry'}} position={LIA_SIT} rotationY={Math.PI} pose={{time: t, sit: 1, headPitch: 0.25 + Math.sin(t * 9) * 0.03}} />
			</Stage>
			<Billboards cam={cam} t={t} items={[{p: [LIA_SIT[0], LIA_SIT[1] - 1, LIA_SIT[2]], talking: talking('lia', t)}]} />
			<GameUI t={t} talking={talking('lia', t)} mode="lobby" lobbyEnds={0} chatFrom={71.0} />
			<AbsoluteFill style={{background: '#1b2a4a', mixBlendMode: 'multiply', opacity: 0.35}} />
			<AbsoluteFill style={{background: '#000', opacity: 1 - clamp01((t - t0) / 0.6)}} />
		</AbsoluteFill>
	);
};

// ================================================================ BoompjeJunior arrives
const BEAM: V3 = [0, Y, -6];
const STOP: V3 = [0, Y, 16.6];
const WALK0 = 85.6;
const WALK1 = 92.6;
const WORDS = {tall: 86.9, strong: 87.5, dutch: 88.24};

const boompPos = (t: number): V3 => lerp3(BEAM, STOP, range(t, WALK0, WALK1));
const dutchPop = (t: number) => {
	const k = clamp01((t - WORDS.dutch) / 0.35);
	return k <= 0 ? 0 : 1 + Math.sin(k * Math.PI) * 0.15 * (1 - k) + (k < 1 ? -(1 - easeOut(k)) : 0);
};

const DutchStuff: React.FC<{t: number}> = ({t}) => {
	const s = dutchPop(t);
	if (s <= 0) return null;
	return (
		<>
			<group scale={[1, s, 1]}>
				<Windmill position={[22, 0, -44]} t={t} s={1.6} rotationY={-0.4} />
				<Windmill position={[-30, 0, -56]} t={t + 2} s={1.3} rotationY={0.3} />
				<Tulips center={[0, 0, -34]} w={60} d={5} rows={5} />
			</group>
			<DutchFlag position={[-11, Y, -20]} t={t} s={s} />
			<DutchFlag position={[11, Y, -20]} t={t + 1} s={s} />
		</>
	);
};

const ARR_SHOTS: Shot[] = [
	{from: 84, to: 85.6, cam: (t, k) => ({pos: lerp3([1.8, 6.4, 27], [1.4, 6.0, 25.5], k), target: [0, 5, -4], fov: 50})},
	{
		from: 85.6,
		to: WORDS.tall,
		cam: (t, k) => {
			const b = boompPos(t);
			return {pos: [b[0] + 1.4 - k * 0.4, 3.0, b[2] + 8.0 - k * 0.6], target: [b[0], 4.8, b[2]], fov: 46};
		},
	},
	{
		from: WORDS.tall,
		to: WORDS.strong,
		cam: (t) => {
			const b = boompPos(t);
			return {pos: [b[0] + 0.6, 0.9, b[2] + 4.2], target: [b[0], 7.0, b[2]], fov: 62};
		},
	},
	{
		from: WORDS.strong,
		to: WORDS.dutch,
		cam: (t, k) => {
			const b = boompPos(t);
			return {pos: [b[0] + 7.2 - k * 0.6, 4.8, b[2] + 5.0], target: [b[0], 4.6, b[2]], fov: 44};
		},
	},
	{
		from: WORDS.dutch,
		to: 89.4,
		cam: (t, k) => {
			const b = boompPos(t);
			return {pos: [b[0] - 3.5, 4.5 + k * 1.5, b[2] + 13 + k], target: [6, 7, -34], fov: 54};
		},
	},
	{
		from: 89.4,
		to: 92.6,
		cam: (t, k) => {
			const b = boompPos(t);
			return {pos: [13, 6.5, b[2] + 3], target: [0, 4, b[2] + 1.5], fov: 50};
		},
	},
	{from: 92.6, to: 95.0, cam: (t, k) => ({pos: lerp3([3.6, 4.9, 24.0], [3.2, 4.8, 23.4], k), target: [0, 5.6, STOP[2]], fov: 44})},
	{from: 95.0, to: 96.4, cam: (t, k) => ({pos: lerp3([0.9, 4.25, 17.6], [0.6, 4.2, 18.2], ease(k)), target: [0, 4.0, LIA_SIT[2]], fov: 38})},
];

const MapCard: React.FC<{t: number; from: number; to: number}> = ({t, from, to}) => {
	if (t < from || t > to) return null;
	const k = easeOut((t - from) / 0.35);
	const o = interpolate(t, [from, from + 0.15, to - 0.25, to], [0, 1, 1, 0]);
	const line = clamp01((t - from - 0.4) / 0.9);
	return (
		<div style={{position: 'absolute', right: 170, top: 170, width: 520, opacity: o, transform: `translateX(${(1 - k) * 80}px) rotate(2deg)`}}>
			<div style={{borderRadius: 26, overflow: 'hidden', background: '#e8eef2', border: '6px solid #fff', boxShadow: '0 20px 50px rgba(0,0,0,0.5)'}}>
				<div style={{position: 'relative', height: 300, background: '#dfe7d5'}}>
					{/* roads */}
					{[
						[0, 80, 520, 22, 0],
						[0, 200, 520, 18, 0],
						[140, 0, 20, 300, 0],
						[360, 0, 24, 300, 0],
						[-40, 140, 640, 16, -18],
					].map(([x, y, w, h, r], i) => (
						<div key={i} style={{position: 'absolute', left: x, top: y, width: w, height: h, background: '#fff', transform: `rotate(${r}deg)`, boxShadow: '0 0 0 2px #cfd8dc'}} />
					))}
					<div style={{position: 'absolute', left: 30, top: 10, width: 90, height: 60, borderRadius: 10, background: '#a5d6a7'}} />
					<div style={{position: 'absolute', left: 400, top: 230, width: 100, height: 60, borderRadius: 30, background: '#90caf9'}} />
					{/* route */}
					<svg width="520" height="300" style={{position: 'absolute', left: 0, top: 0}}>
						<path d="M 90 240 L 150 210 L 150 90 L 372 90 L 430 60" fill="none" stroke="#2f7cf6" strokeWidth="10" strokeLinecap="round" strokeLinejoin="round" strokeDasharray="600" strokeDashoffset={600 * (1 - line)} />
					</svg>
					{[
						[90, 240, '#ff4fa3', 'Lia'],
						[430, 60, '#7f539e', 'Boompje'],
					].map(([x, y, c, n]) => (
						<div key={n as string} style={{position: 'absolute', left: (x as number) - 22, top: (y as number) - 52}}>
							<div style={{width: 44, height: 44, borderRadius: '50% 50% 50% 0', transform: 'rotate(-45deg)', background: c as string, border: '4px solid #fff'}} />
							<div style={{position: 'absolute', left: 52, top: 4, fontFamily: UI_FONT, fontWeight: 800, fontSize: 24, color: '#263238', whiteSpace: 'nowrap'}}>{n}</div>
						</div>
					))}
				</div>
				<div style={{padding: '16px 26px', display: 'flex', alignItems: 'center', gap: 16, fontFamily: UI_FONT, color: '#263238'}}>
					<span style={{fontSize: 46, fontFamily: '"Noto Color Emoji"'}}>🚗</span>
					<div>
						<div style={{fontSize: 44, fontWeight: 800, color: '#1e8e3e'}}>20 min</div>
						<div style={{fontSize: 24, fontWeight: 600, color: '#607d8b'}}>Fastest route · basically neighbours</div>
					</div>
				</div>
			</div>
		</div>
	);
};

export const ArrivalScene: React.FC<{t0: number}> = ({t0}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const {cam: base} = shotAt(ARR_SHOTS, t);
	const cam = withShake(base, t, t > WORDS.dutch && t < WORDS.dutch + 0.4 ? 0.12 * (1 - (t - WORDS.dutch) / 0.4) : 0);
	const envK = ease(range(t, 84.0, 86.2));
	const env = {...lerpEnv(LOBBY_NIGHT, LOBBY_SUNSET, envK), shadowCenter: [0, 0, 6] as V3, shadowSize: 40};
	const beamK = ease(range(t, 84.0, 84.6)) * (1 - ease(range(t, 89.0, 90.4)));
	const appear = easeOut(range(t, 84.35, 84.9));
	const b = boompPos(t);
	const walking = t > WALK0 && t < WALK1;
	const walkAmt = walking ? Math.min(1, (t - WALK0) * 3, (WALK1 - t) * 3) : 0;
	const flex = range(t, WORDS.strong, WORDS.strong + 0.2) * (1 - range(t, WORDS.dutch - 0.05, WORDS.dutch + 0.25));
	const liaFace: Look['face'] = t < 84.6 ? 'liacry' : t < 95.2 ? 'liashock' : 'hearts';
	const liaLook = t < 84.6 ? 0.25 : -0.25 * ease(range(t, 84.6, 85.2));
	const sparkleRing: V3[] =
		t < 86.2
			? new Array(18).fill(0).map((_, j) => {
					const a = j * 0.35 + t * 2;
					return [BEAM[0] + Math.cos(a) * 2.6, 1 + ((j * 0.7 + t * 3) % 8), BEAM[2] + Math.sin(a) * 2.6] as V3;
			  })
			: [];
	const flexSparkles: V3[] = flex > 0.5 ? new Array(12).fill(0).map((_, j) => [b[0] + (j % 2 ? 2.6 : -2.6) + Math.sin(t * 8 + j) * 0.6, 5.8 + Math.cos(t * 7 + j) * 0.8, b[2] + Math.sin(j) * 0.6] as V3) : [];
	const sub = t >= WORDS.dutch ? 'TALL. STRONG. DUTCH. 🇳🇱' : t >= WORDS.strong ? 'TALL. STRONG.' : t >= WORDS.tall ? 'TALL.' : '';
	const pulse = t > 95.0 && t < 96.4 ? Math.max(0, Math.sin((t - 95.0) * Math.PI * 2 * 1.25)) : 0;
	return (
		<AbsoluteFill>
			<Stage cam={cam} env={env}>
				<Lobby lampsOn={1 - envK} t={t} />
				<Clouds t={t} color={envK > 0.5 ? '#ffd6e6' : '#2a3045'} opacity={0.85} />
				{t < 84.5 ? <Rain t={t} center={[0, 0, 14]} area={70} count={1400} opacity={0.45 * (1 - range(t, 84.0, 84.5))} /> : null}
				<LightBeam position={BEAM} k={beamK} />
				<Sparkles points={sparkleRing} t={t} color="#fff3b0" size={0.3} />
				<Sparkles points={flexSparkles} t={t} color="#ffffff" size={0.35} />
				<DutchStuff t={t} />
				<Avatar look={{...LIA_LOOK, face: liaFace}} position={LIA_SIT} rotationY={Math.PI} pose={{time: t, sit: 1, headPitch: liaLook}} />
				{appear > 0 ? (
					<Avatar
						look={{...BOOMP_LOOK, face: t > 93.8 && t < 94.3 ? 'duckwink' : 'duck'}}
						position={b}
						scale={appear}
						rotationY={0}
						pose={{walk: (t - WALK0) * 5, walkAmt, time: t, flex, headPitch: t > 92.6 ? 0.18 : 0}}
					/>
				) : null}
				{t > 95.2 ? <Petals t={t} center={[0, 0, 18]} area={24} count={120} /> : null}
			</Stage>
			<Billboards
				cam={cam}
				t={t}
				items={[
					{p: [LIA_SIT[0], LIA_SIT[1] - 1, LIA_SIT[2]], talking: talking('lia', t), hearts: t > 95.3 ? t - 95.3 : undefined},
					...(appear > 0.9 ? [{p: b, name: 'BoompjeJunior', talking: talking('boomp', t), bubble: talking('boomp', t) ? null : bubbleOf('BoompjeJunior', t), h: 6.0} as BB] : []),
				]}
			/>
			<GameUI t={t} talking={talking('lia', t)} mode="lobby" lobbyEnds={0} chatFrom={71.0} />
			<NameCard t={t} at={85.7} dur={89.3 - 85.7} name="BOOMPJEJUNIOR" sub={sub} color="#b26bff" />
			<MapCard t={t} from={89.5} to={92.5} />
			{/* rain tint fades out, heartbeat pulse */}
			<AbsoluteFill style={{background: '#1b2a4a', mixBlendMode: 'multiply', opacity: 0.35 * (1 - envK)}} />
			<AbsoluteFill style={{boxShadow: `inset 0 0 ${200 + pulse * 120}px rgba(255,60,140,${0.55 * pulse})`}} />
		</AbsoluteFill>
	);
};

// ================================================================ love + 67 kids
const CENTER: V3 = [0, Y, 8];
const LIA_C: V3 = [-1.8, Y, 8];
const BOOMP_C: V3 = [2.0, Y, 8];
const KIDS = (() => {
	const out: {p: V3; i: number}[] = [];
	const rings: [number, number][] = [
		[5.2, 10],
		[7.6, 15],
		[10.0, 20],
		[12.4, 22],
	];
	let i = 0;
	rings.forEach(([r, n], ri) => {
		for (let k = 0; k < n; k++) {
			const a = (k / n) * Math.PI * 2 + ri * 0.4;
			out.push({p: [CENTER[0] + Math.cos(a) * r + (rand(i) - 0.5) * 0.8, Y, CENTER[2] + Math.sin(a) * r + (rand(i + 9) - 0.5) * 0.8], i: i++});
		}
	});
	return out;
})();

export const FRIENDS_BACK: {name: string; look: Look; p: V3; at: number}[] = [
	{name: 'REQ', look: REQ_LOOK, p: [-6.5, Y, 23.5], at: 108.6},
	{name: 'Mikey', look: MIKEY_LOOK, p: [-2.4, Y, 24.4], at: 108.9},
	{name: 'Ade', look: ADE_LOOK, p: [2.2, Y, 24.4], at: 109.2},
	{name: 'lojjkli', look: KLI_MM2, p: [6.5, Y, 23.5], at: 109.5},
];
const REQ_P = FRIENDS_BACK[0].p;

const popScale = (t: number, at: number) => {
	const k = clamp01((t - at) / 0.28);
	if (k <= 0) return 0;
	return 1 + 2.70158 * Math.pow(k - 1, 3) + 1.70158 * Math.pow(k - 1, 2);
};

const Kids: React.FC<{t: number; panic: number; lookAt?: V3 | null}> = ({t, panic, lookAt}) => {
	const looks = useMemo(() => KIDS.map((k) => kidLook(k.i)), []);
	return (
		<>
			{KIDS.map((k, n) => {
				const s = popScale(t, KID_POP(n));
				if (s <= 0) return null;
				const run = panic > 0 ? (t - 119.2) * (3 + rand(n) * 2) : 0;
				const away = Math.atan2(k.p[0] - REQ_P[0], k.p[2] - REQ_P[2]) + (rand(n + 4) - 0.5) * 0.8;
				const p: V3 = panic > 0 ? [k.p[0] + Math.sin(away) * run, Y, k.p[2] + Math.cos(away) * run] : k.p;
				const yaw = panic > 0 ? away : lookAt ? face(k.p, lookAt) : face(k.p, CENTER);
				const dance = t < 115.2;
				return (
					<Avatar
						key={k.i}
						look={looks[n]}
						position={p}
						scale={0.45 * s}
						rotationY={yaw}
						pose={{
							time: t + n * 0.37,
							sixSeven: dance && t > KID_POP(n) + 0.3 ? 1 : 0,
							jump: dance ? Math.abs(Math.sin(t * 6 + n)) * 1.6 : 0,
							walk: t * 14 + n,
							walkAmt: panic,
							armsUp: panic,
						}}
					/>
				);
			})}
		</>
	);
};

const LOVE_SHOTS: Shot[] = [
	{
		from: 96.4,
		to: 99.6,
		cam: (t, k) => {
			const a = lerp(-0.5, 0.7, k);
			return {pos: [CENTER[0] + Math.sin(a) * 11, lerp(5.5, 6.5, k), CENTER[2] + Math.cos(a) * 11], target: [0, 4.4, 8], fov: 46};
		},
	},
	{from: 99.6, to: 101.1, cam: (t, k) => ({pos: lerp3([5.6, 6.4, 11.8], [5.2, 6.3, 11.3], k), target: [LIA_C[0], 4.6, LIA_C[2]], fov: 40})},
	{from: 101.1, to: 102.5, cam: (t, k) => ({pos: lerp3([-5.8, 6.6, 4.4], [-5.4, 6.5, 4.8], k), target: [BOOMP_C[0], 5.0, BOOMP_C[2]], fov: 40})},
	{from: 102.5, to: 104.0, cam: (t) => ({pos: [3.8, 6.2, 1.2], target: [LIA_C[0], 3.9, LIA_C[2]], fov: t > 103.28 ? lerp(44, 34, easeOut(range(t, 103.28, 103.42))) : 44})},
	{from: 104.0, to: 106.6, cam: (t, k) => ({pos: lerp3([0, 15, 32], [0, 21, 36], ease(k)), target: [0, 2, 7], fov: 50})},
	{
		from: 106.6,
		to: 110,
		cam: (t, k) => {
			const a = lerp(0.9, 0.2, k);
			return {pos: [Math.sin(a) * 20, lerp(12, 8, ease(k)), 8 + Math.cos(a) * 20], target: [0, 2.6, 9], fov: 52};
		},
	},
];

export const LoveScene: React.FC<{t0: number}> = ({t0}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const {cam: base} = shotAt(LOVE_SHOTS, t);
	const cam = withShake(base, t, t > 103.28 && t < 103.8 ? 0.1 * (1 - (t - 103.28) / 0.5) : 0);
	const env = {...LOBBY_SUNSET, shadowCenter: [0, 0, 8] as V3, shadowSize: 30};
	const kidsIn = KIDS.filter((_, n) => t >= KID_POP(n)).length;
	const lia67 = range(t, 102.6, 102.8);
	const heartsAt = (base: number) => (t > base ? (t - base) % 2.5 : undefined);
	return (
		<AbsoluteFill>
			<Stage cam={cam} env={env}>
				<Lobby t={t} />
				<Clouds t={t} color="#ffd6e6" opacity={0.85} />
				<DutchStuff t={t} />
				<Petals t={t} center={[0, 0, 8]} area={34} />
				<Avatar look={{...LIA_LOOK, face: 'hearts'}} position={LIA_C} rotationY={Math.PI / 2} pose={{time: t, sixSeven: lia67, jump: t > 104 && t < 106.6 ? Math.abs(Math.sin(t * 6)) * 1.0 : 0}} />
				<Avatar look={{...BOOMP_LOOK, face: t > 101.0 && t < 101.4 ? 'duckwink' : 'duck'}} position={BOOMP_C} rotationY={-Math.PI / 2} pose={{time: t, headPitch: 0.15, headYaw: t > 101.2 && t < 102.4 ? 0.25 : 0}} />
				<Kids t={t} panic={0} />
				<Sparkles points={KIDS.filter((_, n) => t > KID_POP(n) && t < KID_POP(n) + 0.4).flatMap((k, j) => [0, 1, 2].map((q) => [k.p[0] + Math.cos(q * 2 + j) * 1.2, 1.2 + q * 0.6, k.p[2] + Math.sin(q * 2 + j) * 1.2] as V3))} t={t} color="#ffe6f6" size={0.25} />
				{FRIENDS_BACK.map((f, i) => {
					const s = popScale(t, f.at);
					return s > 0 ? <Avatar key={f.name} look={f.look} position={f.p} scale={s} rotationY={face(f.p, CENTER)} pose={{time: t + i}} /> : null;
				})}
			</Stage>
			<Billboards
				cam={cam}
				t={t}
				items={[
					{p: LIA_C, talking: talking('lia', t), hearts: t < 104 ? heartsAt(96.6) : undefined},
					{p: BOOMP_C, name: 'BoompjeJunior', talking: talking('boomp', t), bubble: talking('boomp', t) ? null : bubbleOf('BoompjeJunior', t), hearts: t < 104 ? heartsAt(96.9) : undefined, h: 6.0},
					...FRIENDS_BACK.filter((f) => t > f.at + 0.2).map((f) => ({p: f.p, name: f.name})),
				]}
			/>
			<GameUI t={t} talking={talking('lia', t)} mode="lobby" lobbyEnds={0} chatFrom={96.0} />
			<BigText t={t} from={103.28} to={104.4} text="6  7" color="#ffe14d" top={120} size={190} />
			{t >= 104.0 ? (
				<div style={{position: 'absolute', left: 0, right: 0, top: 110, textAlign: 'center', opacity: interpolate(t, [104.0, 104.2, 109.6, 110], [0, 1, 1, 0])}}>
					<span style={{fontFamily: GAME_FONT, fontWeight: 700, fontSize: 92, color: '#ff8fd0', WebkitTextStroke: '13px #3a0a24', paintOrder: 'stroke fill'}}>
						👶 KIDS: {kidsIn}
						<span style={{color: '#fff', fontSize: 60}}>/67</span>
					</span>
				</div>
			) : null}
		</AbsoluteFill>
	);
};

// ================================================================ party, fart, end of the world
const KLI_P = FRIENDS_BACK[3].p;
const FART = 115.2;
const GAS0 = 118.6;

const PARTY_SHOTS: Shot[] = [
	{
		from: 110,
		to: 112.9,
		cam: (t, k) => {
			const a = lerp(-0.45, 0.05, k);
			return {pos: [Math.sin(a) * 30, 12, 8 + Math.cos(a) * 30], target: [0, 3, 12], fov: 50};
		},
	},
	{from: 112.9, to: 115.0, cam: (t, k) => ({pos: lerp3([-4.2, 5.0, 18.8], [-4.6, 4.95, 19.6], k), target: [REQ_P[0], 4.6, REQ_P[2]], fov: 40})},
	{from: 115.0, to: 116.2, cam: (t, k) => ({pos: lerp3([REQ_P[0] - 6.4, 4.4, REQ_P[2] + 3.2], [REQ_P[0] - 5.8, 4.2, REQ_P[2] + 2.8], k), target: [REQ_P[0] + 0.2, 3.2, REQ_P[2] + 0.6], fov: 48})},
	{from: 116.2, to: 117.4, cam: (t, k) => ({pos: lerp3([-7.4, 6.4, 26.4], [-7.6, 6.6, 27.0], k), target: [0, 3, 10], fov: 52})},
	{from: 117.4, to: 118.6, cam: (t, k) => ({pos: lerp3([1.0, 5.3, 21.2], [1.5, 5.2, 21.5], k), target: [KLI_P[0], 4.5, KLI_P[2]], fov: 44})},
	{from: 118.6, to: 121.4, cam: (t, k) => ({pos: lerp3([4, 16, 52], [0, 28, 70], ease(k)), target: [0, 2, 10], fov: 52})},
	{from: 121.4, to: 123.6, cam: (t, k) => ({pos: lerp3([0, 28, 70], [0, 38, 84], k), target: [0, 2, 6], fov: 54})},
];

export const PartyScene: React.FC<{t0: number}> = ({t0}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const {cam: base} = shotAt(PARTY_SHOTS, t);
	const quake = 0.05 * range(t, 119, 121) + 0.35 * range(t, 121.4, 123.4);
	const cam = withShake(base, t, quake + (t > FART && t < FART + 0.5 ? 0.04 : 0));
	const toxic = ease(range(t, 118.8, 120.6));
	const env = {...lerpEnv(LOBBY_SUNSET, TOXIC, toxic), shadowCenter: [0, 0, 10] as V3, shadowSize: 34};
	const panic = range(t, 119.2, 119.6);
	const turned = t > 116.2;
	const lookReq = turned ? REQ_P : null;
	const gasR = t > GAS0 ? 2 + Math.pow(t - GAS0, 1.3) * 5 : 0;
	const reqFace: Look['face'] = t < 113.8 ? 'smile' : t < FART + 0.2 ? 'sick' : t < 119 ? 'grin' : 'scream';
	const shock = turned && t < 119.2;
	const who = [
		...FRIENDS_BACK.map((f) => ({name: f.name, look: f.look, p: f.p})),
		{name: 'Lia', look: LIA_LOOK, p: LIA_C},
		{name: 'BoompjeJunior', look: BOOMP_LOOK, p: BOOMP_C},
	];
	const run = (p: V3, i: number): V3 => {
		if (panic <= 0) return p;
		const away = Math.atan2(p[0] - REQ_P[0], p[2] - REQ_P[2]) + (rand(i + 50) - 0.5) * 0.6;
		const d = (t - 119.2) * 4.5;
		return [p[0] + Math.sin(away) * d, Y, p[2] + Math.cos(away) * d];
	};
	const faceFor = (name: string, def: Look['face']): Look['face'] => {
		if (name === 'REQ') return reqFace;
		if (t > 119.2) return name === 'Lia' ? 'liashock' : name === 'lojjkli' ? 'kliwide' : 'scream';
		if (shock) return name === 'Lia' ? 'liashock' : name === 'lojjkli' ? 'kli' : name === 'BoompjeJunior' ? 'duck' : 'shock';
		return def;
	};
	return (
		<AbsoluteFill>
			<Stage cam={cam} env={env}>
				<Lobby t={t} />
				<Clouds t={t} color={toxic > 0.5 ? '#3c5a10' : '#ffd6e6'} opacity={0.85} />
				<DutchStuff t={t} />
				{toxic < 0.6 ? <Petals t={t} center={[0, 0, 8]} area={34} count={100} /> : null}
				<Kids t={t} panic={panic} lookAt={lookReq} />
				{who.map((w, i) => {
					const p = run(w.p, i);
					const yaw = panic > 0 ? Math.atan2(p[0] - REQ_P[0], p[2] - REQ_P[2]) : w.name === 'REQ' ? face(w.p, CENTER) : turned ? face(w.p, REQ_P) : w.name === 'Lia' ? Math.PI / 2 : w.name === 'BoompjeJunior' ? -Math.PI / 2 : face(w.p, CENTER);
					return (
						<Avatar
							key={w.name}
							look={{...w.look, face: faceFor(w.name, w.look.face)}}
							position={p}
							rotationY={yaw}
							pose={{
								time: t + i,
								walk: t * 14 + i,
								walkAmt: panic,
								armsUp: panic,
								jump: w.name === 'REQ' && t > FART && t < FART + 0.4 ? Math.sin(((t - FART) / 0.4) * Math.PI) * 0.8 : t < 113 && w.name !== 'REQ' ? Math.abs(Math.sin(t * 5 + i)) * 0.6 : 0,
								sixSeven: t < 113 && (w.name === 'Mikey' || w.name === 'Ade') ? 1 : 0,
							}}
						/>
					);
				})}
				<group position={REQ_P} rotation={[0, face(REQ_P, CENTER), 0]}>
					<StinkPuffs position={[0, 0, 0]} k={t - FART} />
				</group>
				<GasCloud center={REQ_P} r={gasR} t={t} opacity={0.42} />
			</Stage>
			<Billboards
				cam={cam}
				t={t}
				items={[
					...who
						.filter((w) => w.name !== 'Lia')
						.map((w, i) => ({
							p: run(w.p, who.indexOf(w)),
							name: w.name,
							h: w.name === 'BoompjeJunior' ? 6.0 : 5.7,
							talking: (w.name === 'REQ' && talking('req', t)) || (w.name === 'lojjkli' && talking('kli', t)),
							bubble: bubbleOf(w.name, t),
							emote: t > 116.3 && t < 118.4 && w.name !== 'REQ' ? {char: ['😳', '🤢', '💀', '😐', '🤢'][i % 5], age: t - 116.3 - i * 0.08} : null,
						})),
					{p: run(LIA_C, 4), talking: talking('lia', t)},
				]}
			/>
			<GameUI t={t} talking={talking('lia', t)} mode="lobby" lobbyEnds={0} chatFrom={108.0} />
			<AlertBanner t={t} from={119.3} text="⚠️ SERVER ALERT: TOXIC GAS LEVELS CRITICAL ⚠️" />
			<AbsoluteFill style={{background: '#7dff2a', mixBlendMode: 'multiply', opacity: toxic * 0.25}} />
			<AbsoluteFill style={{background: '#fff', opacity: range(t, 123.15, 123.6)}} />
		</AbsoluteFill>
	);
};
