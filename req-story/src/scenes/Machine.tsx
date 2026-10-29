import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {Avatar, Look, NPC_NAMES, npcLook, REQ_LOOK} from '../three/Avatar';
import {Cam, clamp01, ease, easeOut, lerp3, range, shake, V3} from '../three/cam';
import {LampPost, Machine, Pet, Rain} from '../three/Props';
import {Clouds, DAY, Env, Forest, Ground, Stage} from '../three/World';
import {FPS, reqTalking, TAPS} from '../timeline';
import {Billboards} from '../ui/Billboards';
import {DayCard, GameButton, GameUI, Toast, ZoneBanner} from '../ui/HUD';
import {PurchasePrompt} from '../ui/Dialogs';
import {FaceKind} from '../three/textures';

// ---------------------------------------------------------------- reels
type Spin = {start: number; stops: [number, number, number]; final: [number, number, number]};
const SPINS: Spin[] = [
	{start: 27.5, stops: [28.5, 28.9, 29.3], final: [0, 4, 3]},
	{start: 31.6, stops: [32.2, 32.6, 33.0], final: [2, 1, 4]},
	{start: 34.35, stops: [34.75, 34.9, 35.05], final: [5, 4, 0]},
	{start: 35.35, stops: [35.75, 35.9, 36.05], final: [3, 2, 4]},
	{start: 36.35, stops: [36.75, 36.9, 37.05], final: [4, 0, 1]},
	{start: 38.3, stops: [38.8, 39.1, 39.4], final: [1, 3, 2]},
	{start: 39.9, stops: [40.4, 40.7, 41.0], final: [0, 0, 4]},
	// near miss: diamond, diamond... skull
	{start: 45.5, stops: [46.0, 46.4, 46.95], final: [1, 1, 4]},
];

const mod = (a: number, n: number) => ((a % n) + n) % n;

export const reelsAt = (t: number): [number, number, number] => {
	const out: [number, number, number] = [2, 2, 2];
	let prev: [number, number, number] = [2, 2, 2];
	for (const s of SPINS) {
		if (t < s.start) break;
		for (let i = 0; i < 3; i++) {
			if (t >= s.stops[i]) out[i] = s.final[i];
			else {
				const u = (t - s.start) / (s.stops[i] - s.start);
				const R = 6 * (2 + i) + mod(s.final[i] - prev[i], 6);
				out[i] = prev[i] + R * easeOut(u);
			}
		}
		prev = [...s.final] as [number, number, number];
	}
	return out;
};

const spinning = (t: number) => SPINS.some((s) => t >= s.start && t < s.stops[2]);

// ---------------------------------------------------------------- environments
const MORNING: Env = {
	...DAY,
	skyTop: '#5b8fd6',
	skyHorizon: '#ffd7b0',
	sunDir: [-0.7, 0.35, 0.3],
	sunColor: '#ffd9a8',
	sunIntensity: 2.2,
	fog: ['#f3d9c4', 120, 420],
};
const SUNSET: Env = {
	...DAY,
	skyTop: '#3b3d8f',
	skyHorizon: '#ff9a62',
	sunDir: [0.8, 0.15, -0.4],
	sunColor: '#ffad6b',
	sunIntensity: 2.0,
	hemiSky: '#ffb78a',
	hemiGround: '#4a3a5a',
	hemiIntensity: 0.7,
	fog: ['#f2a07a', 100, 380],
	sunGlow: 1.2,
};
export const NIGHT: Env = {
	...DAY,
	skyTop: '#03061a',
	skyHorizon: '#18214a',
	sunDir: [0.3, 0.7, -0.6],
	sunColor: '#9fb4ff',
	sunIntensity: 0.35,
	hemiSky: '#334477',
	hemiGround: '#111522',
	hemiIntensity: 0.45,
	fog: ['#141b38', 80, 300],
	sunGlow: 0.2,
	stars: 1,
};
const RAIN: Env = {...NIGHT, skyTop: '#05070f', skyHorizon: '#1d2333', fog: ['#1b2130', 40, 180], stars: 0, hemiIntensity: 0.4};

type Shot = {from: number; to: number; env: Env; cam: (t: number, k: number) => Cam; face?: FaceKind; day?: number};

const behind = (t: number, k: number, push = 0): Cam => ({
	pos: [4 + Math.sin(t * 0.6) * 0.5, 8.5 - push * 0.8, 25 - push * 2.5],
	target: [0, 6.8, 0],
	fov: 55,
});

const SHOTS: Shot[] = [
	{from: 23.0, to: 25.4, env: DAY, cam: (t, k) => ({pos: lerp3([-18, 2.5, 32], [-7, 8, 24], ease(k)), target: lerp3([0, 11, 0], [0, 9, 0], ease(k)), fov: 52})},
	{
		from: 25.4,
		to: 33.4,
		env: DAY,
		cam: (t) => behind(t, 0, range(t, 27.4, 28.2) - range(t, 29.6, 30.4) + range(t, 31.5, 32.1) - range(t, 33.1, 33.4)),
		face: 'grin',
	},
	{from: 33.4, to: 34.3, env: MORNING, day: 2, face: 'grin', cam: (t, k) => ({pos: lerp3([-15, 6, 17], [-13, 6, 15], k), target: [0, 7, 4], fov: 50})},
	{from: 34.3, to: 35.3, env: DAY, day: 9, face: 'smile', cam: (t, k) => ({pos: lerp3([13, 2.5, 16], [12, 2.8, 14], k), target: [0, 8, 2], fov: 50})},
	{from: 35.3, to: 36.3, env: SUNSET, day: 27, face: 'worried', cam: (t, k) => ({pos: lerp3([-4, 2.8, 24], [-3.5, 3, 22], k), target: [0, 6.5, 4], fov: 50})},
	{from: 36.3, to: 37.2, env: NIGHT, day: 63, face: 'worried', cam: (t, k) => ({pos: lerp3([3.5, 7, 21], [3, 7, 19.5], k), target: [0, 5.5, 0], fov: 52})},
	{from: 37.2, to: 40.0, env: NIGHT, face: 'grin', cam: (t) => behind(t, 0, range(t, 38.2, 38.8) * 0.8)},
	{
		from: 40.0,
		to: 43.7,
		env: NIGHT,
		face: 'grin',
		cam: (t, k) => ({pos: lerp3([1.8, 5.4, 3.2], [1.2, 5.1, 5.0], ease(k)), target: [0, 4.75, 10], fov: 45}),
	},
	{from: 43.7, to: 45.4, env: NIGHT, face: 'worried', cam: (t) => behind(t, 0)},
	{
		from: 45.4,
		to: 48.01,
		env: NIGHT,
		face: 'worried',
		cam: (t, k) => {
			const c: Cam = {pos: lerp3([0, 8.6, 13.5], [0, 8.6, 10.5], ease(range(t, 45.4, 46.9))), target: [0, 8.6, 0], fov: 50};
			const s = shake(t, t > 46.95 ? 0.15 * (1 - range(t, 46.95, 47.6)) : 0);
			c.pos = [c.pos[0] + s[0], c.pos[1] + s[1], c.pos[2]];
			return c;
		},
	},
];

const RESULTS: [number, string, number?][] = [
	[29.4, 'YOU LOST 💀'],
	[33.1, 'YOU LOST 💀', 1.0],
	[35.1, 'LOST', 0.6],
	[36.1, 'LOST', 0.6],
	[37.1, 'LOST', 0.6],
	[39.5, 'LOST 💀', 0.9],
	[41.1, 'LOST 💀', 1.2],
	[47.0, 'SO CLOSE!! 💀'],
];

const REQ_POS: V3 = [0, 0, 10];
const WATCHERS: {p: V3; i: number}[] = [
	{p: [-10, 0, 15], i: 2},
	{p: [10, 0, 17], i: 3},
	{p: [-13, 0, 6], i: 4},
];

const MachineSet: React.FC<{t: number; env: Env; lights?: number; pets?: boolean; reqLook: Look; reqPose: Parameters<typeof Avatar>[0]['pose']; rain?: boolean; watchers?: boolean}> = ({
	t,
	env,
	lights = 1,
	pets = true,
	reqLook,
	reqPose,
	rain,
	watchers = true,
}) => (
	<>
		<Ground />
		<Forest count={40} radius={[34, 170]} seed={5} />
		<Clouds t={t} opacity={env.stars ? 0.15 : 0.9} color={env.stars ? '#445' : '#fff'} />
		<Machine t={t} spin={reelsAt(t)} lights={lights} />
		<Avatar look={reqLook} position={REQ_POS} rotationY={Math.PI} pose={reqPose} />
		{pets ? (
			<>
				<Pet kind="cat" position={[-3.2, 0, 13]} rotationY={Math.PI} t={t} />
				<Pet kind="dog" position={[3.2, 0, 13.5]} rotationY={Math.PI} t={t + 1} />
			</>
		) : null}
		{watchers
			? WATCHERS.map((w) => <Avatar key={w.i} look={npcLook(w.i)} position={w.p} rotationY={Math.atan2(-w.p[0], -w.p[2])} pose={{time: t + w.i}} />)
			: null}
		{rain ? (
			<>
				<Rain t={t} center={[0, 0, 10]} />
				<LampPost position={[4.5, 0, 12.5]} />
			</>
		) : null}
	</>
);

export const MachineScene: React.FC<{t0: number}> = ({t0}) => {
	const frame = useCurrentFrame();
	const t = t0 + frame / FPS;
	const shot = SHOTS.find((s) => t >= s.from && t < s.to) ?? SHOTS[SHOTS.length - 1];
	const k = clamp01((t - shot.from) / (shot.to - shot.from));
	const cam = shot.cam(t, k);
	const env: Env = {...shot.env, shadowCenter: [0, 0, 6], shadowSize: 30};
	const tap = TAPS.find(([at]) => t >= at - 0.1 && t < at + 0.15);
	const look: Look = {...REQ_LOOK, face: shot.face ?? 'smile'};
	const leaning = spinning(t) ? 0.12 : 0;
	const showSpin = (t > 26.9 && t < 43.7) || (t > 45.3 && t < 47.6);
	const pressed = !!tap && tap[2] > 700;
	return (
		<AbsoluteFill>
			<Stage cam={cam} env={env}>
				<MachineSet t={t} env={env} reqLook={look} reqPose={{time: t, lean: leaning, headPitch: -0.12}} />
			</Stage>
			<Billboards
				cam={cam}
				t={t}
				items={[{p: REQ_POS, talking: reqTalking(t)}, ...WATCHERS.map((w) => ({p: w.p, name: NPC_NAMES[w.i]}))]}
			/>
			<GameUI t={t} talking={reqTalking(t)} />
			{showSpin ? (
				<GameButton
					x={960}
					y={880}
					pressed={pressed}
					label={
						<>
							SPIN <span style={{fontSize: 38}}>💎 250K</span>
						</>
					}
				/>
			) : null}
			{RESULTS.map(([at, text, dur]) => (
				<Toast key={at} t={t} at={at} text={text} dur={dur ?? 1.6} />
			))}
			<ZoneBanner text="🎰 Casino Zone" t={t} from={23.2} />
			{shot.day ? <DayCard t={t} from={shot.from} to={shot.from + 0.75} day={shot.day} /> : null}
			<PurchasePrompt t={t} from={43.8} buyAt={44.9} to={45.35} />
			{/* hard-cut flash between montage days */}
			{shot.day ? <AbsoluteFill style={{background: '#fff', opacity: Math.max(0, 0.6 - (t - shot.from) * 5)}} /> : null}
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------- sad / rain
export const SadScene: React.FC<{t0: number}> = ({t0}) => {
	const frame = useCurrentFrame();
	const t = t0 + frame / FPS;
	const wide = t < 51.6;
	const cam: Cam = wide
		? {pos: lerp3([22, 7, 24], [19, 6, 21], range(t, 48, 51.6)), target: [0, 5, 6], fov: 48}
		: {pos: lerp3([5, 3.8, 0.5], [3.8, 3.5, 2.6], ease(range(t, 51.6, 56))), target: [0, 2.7, 10], fov: 42};
	const env: Env = {...RAIN, shadowCenter: [0, 0, 8], shadowSize: 30};
	const flicker = 0.25 + (Math.sin(t * 23) > 0.6 ? 0.25 : 0) * (Math.sin(t * 3.1) > 0 ? 1 : 0);
	const tap = TAPS.find(([at]) => t >= at - 0.1 && t < at + 0.15);
	return (
		<AbsoluteFill>
			<AbsoluteFill style={{filter: 'saturate(0.6) contrast(1.05)'}}>
				<Stage cam={cam} env={env}>
					<MachineSet
						t={t}
						env={env}
						lights={flicker}
						pets={false}
						rain
						watchers={false}
						reqLook={{...REQ_LOOK, face: 'sad'}}
						reqPose={{time: t, sit: 1, headPitch: 0.35 - range(t, 54.4, 55.0) * 0.45}}
					/>
				</Stage>
			</AbsoluteFill>
			<Billboards cam={cam} t={t} items={[{p: [REQ_POS[0], REQ_POS[1] - 1, REQ_POS[2]], talking: reqTalking(t)}]} />
			<GameUI t={t} talking={reqTalking(t)} />
			{t > 54.2 ? <GameButton x={960} y={880} disabled pressed={!!tap} label={<>SPIN <span style={{fontSize: 38}}>💎 250K</span></>} /> : null}
			<Toast t={t} at={55.6} text="Not enough diamonds!" size={64} dur={1.2} />
		</AbsoluteFill>
	);
};
