import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {Avatar, KLI_LOOK, Look, NPC_NAMES, npcLook, REQ_LOOK} from '../three/Avatar';
import {Cam, clamp01, ease, lerp, lerp3, range, shake, V3} from '../three/cam';
import {Arch, Bench, Machine, Meteor, Petals, Rain, Sparkles} from '../three/Props';
import {Clouds, DAY, Env, Forest, Ground, lerpEnv, Stage} from '../three/World';
import {FPS, KLI_BUBBLES, reqTalking} from '../timeline';
import {Billboards} from '../ui/Billboards';
import {GameUI} from '../ui/HUD';
import {AlertBanner} from '../ui/Dialogs';
import {NIGHT, reelsAt} from './Machine';

export const SUNSET_PINK: Env = {
	...DAY,
	skyTop: '#46378f',
	skyHorizon: '#ff9fb8',
	sunDir: [-0.2, 0.12, -1],
	sunColor: '#ffb08a',
	sunIntensity: 2.3,
	hemiSky: '#ffc0d0',
	hemiGround: '#4f3a52',
	hemiIntensity: 0.8,
	fog: ['#f7a9b8', 110, 420],
	sunGlow: 1.6,
};

export const RED: Env = {
	...DAY,
	skyTop: '#160202',
	skyHorizon: '#ff4512',
	sunDir: [0.2, 0.22, -1],
	sunColor: '#ff5a2a',
	sunIntensity: 2.4,
	hemiSky: '#ff6a3a',
	hemiGround: '#2a0a05',
	hemiIntensity: 0.75,
	fog: ['#7a1c0a', 60, 260],
	sunGlow: 1.8,
};

const RAINY: Env = {...NIGHT, skyTop: '#05070f', skyHorizon: '#1d2333', fog: ['#1b2130', 40, 180], stars: 0, hemiIntensity: 0.4};

const bubbleFor = (t: number) => {
	const b = [...KLI_BUBBLES].reverse().find((c) => t >= c.at && t < c.at + (c.text.length > 15 ? 2.0 : 2.6));
	return b ? {text: b.text, age: t - b.at} : null;
};

// ---------------------------------------------------------------- kli arrives
const FLY_FROM = 57.6;
const FLY_TO = 60.0;
const KLI_LAND: V3 = [0, 0, 4.6];
const REQ_AT: V3 = [0, 0, 10];

const bez = (a: V3, b: V3, c: V3, d: V3, u: number): V3 => {
	const m = 1 - u;
	return [0, 1, 2].map((i) => m * m * m * a[i] + 3 * m * m * u * b[i] + 3 * m * u * u * c[i] + u * u * u * d[i]) as V3;
};
const kliPath = (t: number): V3 => {
	const u = ease(range(t, FLY_FROM, FLY_TO));
	return bez([150, 85, 30], [70, 50, 34], [22, 14, 14], KLI_LAND, u);
};

export const ArrivalScene: React.FC<{t0: number}> = ({t0}) => {
	const frame = useCurrentFrame();
	const t = t0 + frame / FPS;
	const envK = ease(range(t, 56.2, 58.4));
	const env: Env = {...lerpEnv(RAINY, SUNSET_PINK, envK), shadowCenter: [0, 0, 7], shadowSize: 30};
	const kli = kliPath(t);
	const prev = kliPath(t - 0.05);
	const flying = t < FLY_TO;
	const kliRot = flying ? Math.atan2(kli[0] - prev[0], kli[2] - prev[2]) : 0;
	const flyAmt = flying ? 1 - range(t, FLY_TO - 0.5, FLY_TO) : 0;
	const stand = range(t, 56.9, 57.4);
	const lookUp = t < FLY_TO ? -0.45 * ease(range(t, 57.2, 57.8)) : -0.45 * (1 - ease(range(t, 59.6, 60.3)));
	const shot1 = t < 60.0;
	const cam: Cam = shot1
		? {pos: [-7, 2.6, 21], target: lerp3([10, 14, 0], [kli[0] * 0.75, Math.max(3.5, kli[1] * 0.85), kli[2] * 0.75 + 4], ease(range(t, 57.2, 58.0))), fov: 60}
		: {pos: lerp3([13.5, 5.2, 7.6], [11.5, 5.0, 7.6], range(t, 60, 64.5)), target: [0, 4.3, 7.4], fov: 46};
	const trail: V3[] = flying ? new Array(22).fill(0).map((_, j) => {
		const p = kliPath(t - (j + 1) * 0.035);
		return [p[0] + Math.sin(j * 2.3) * 0.6, p[1] + 3 + Math.cos(j * 1.7) * 0.6, p[2]] as V3;
	}) : [];
	const landBurst: V3[] = t >= FLY_TO && t < FLY_TO + 1.2
		? new Array(14).fill(0).map((_, j) => {
				const a = (j / 14) * Math.PI * 2;
				const r = (t - FLY_TO) * 7;
				return [KLI_LAND[0] + Math.cos(a) * r, 0.6 + (t - FLY_TO) * 2, KLI_LAND[2] + Math.sin(a) * r] as V3;
		  })
		: [];
	return (
		<AbsoluteFill>
			<Stage cam={cam} env={env}>
				<Ground />
				<Forest count={40} radius={[34, 170]} seed={5} />
				<Clouds t={t} opacity={0.3 + envK * 0.6} color={envK > 0.5 ? '#ffd6e6' : '#445'} />
				<Machine t={t} spin={reelsAt(48)} lights={0.25 + envK * 0.5} />
				{t < 57.0 ? <Rain t={t} center={[0, 0, 10]} /> : null}
				<Avatar
					look={{...REQ_LOOK, face: t < 60.4 ? 'sad' : 'happy'}}
					position={REQ_AT}
					rotationY={Math.PI}
					pose={{time: t, sit: 1 - stand, headPitch: lookUp}}
				/>
				<Avatar look={KLI_LOOK} position={kli} rotationY={kliRot} pose={{time: t, fly: flyAmt, wave: t > 61.9 && t < 63 ? 1 : 0}} />
				<Sparkles points={trail} t={t} color="#fff3b0" />
				<Sparkles points={landBurst} t={t} color="#ff9ad5" size={0.4} />
			</Stage>
			<Billboards
				cam={cam}
				t={t}
				items={[
					{p: [REQ_AT[0], REQ_AT[1] - (1 - stand), REQ_AT[2]], talking: reqTalking(t)},
					{p: kli, name: t > 59.0 ? 'lojjkli' : undefined, bubble: bubbleFor(t), hearts: t >= FLY_TO ? t - FLY_TO : undefined},
				]}
			/>
			<GameUI t={t} talking={reqTalking(t)} />
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------- wedding (+ the sky turning red)
export const REQ_WED: Look = {...REQ_LOOK, torso: '#16161c', arms: '#16161c', legs: '#16161c', shirt: 'suit', shirtColor: '#d62828', hat: 'tophat'};
const R_POS: V3 = [-2.4, 0.4, 0];
const K_POS: V3 = [2.4, 0.4, 0];

const GUESTS: {p: V3; i: number}[] = [];
[9, 14, 19].forEach((z, row) =>
	[-1, 1].forEach((side) =>
		[-1.8, 1.8].forEach((dx, k) => {
			GUESTS.push({p: [side * 7 + dx, 0.2, z + 0.3], i: (row * 4 + (side + 1) + k) % 12});
		}),
	),
);

const WeddingSet: React.FC<{t: number; red: number; reqFace: Look['face']; guestsUp: number; cheer: number; petals: boolean}> = ({
	t,
	red,
	reqFace,
	guestsUp,
	cheer,
	petals,
}) => (
	<>
		<Ground />
		<Forest count={44} radius={[30, 170]} seed={8} avoid={(x, z) => Math.abs(x) < 16 && z > -10 && z < 40} />
		<Clouds t={t} color={red > 0.5 ? '#3a0c08' : '#ffd6e6'} opacity={0.85} />
		<Arch />
		{/* aisle */}
		<mesh position={[0, 0.06, 18]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
			<planeGeometry args={[3.4, 28]} />
			<meshStandardMaterial color="#b3123a" roughness={0.9} />
		</mesh>
		{[8, 14, 20, 26].map((z) =>
			[-4.2, 4.2].map((x) => (
				<group key={x + '_' + z} position={[x, 0, z]}>
					<mesh position={[0, 1.6, 0]}>
						<boxGeometry args={[0.3, 3.2, 0.3]} />
						<meshStandardMaterial color="#ffffff" />
					</mesh>
					<mesh position={[0, 3.4, 0]}>
						<sphereGeometry args={[0.45, 14, 10]} />
						<meshStandardMaterial color="#fff2c4" emissive="#ffc46b" emissiveIntensity={2.2} />
					</mesh>
				</group>
			)),
		)}
		{[9, 14, 19].map((z) => [-7, 7].map((x) => <Bench key={x + '_' + z} position={[x, 0, z]} rotationY={Math.PI} />))}
		{GUESTS.map((g, n) => {
			const jump = cheer > 0 ? Math.abs(Math.sin(t * 7 + n)) * 1.2 * cheer : 0;
			return (
				<Avatar
					key={n}
					look={{...npcLook(g.i), face: red > 0.4 ? 'worried' : cheer > 0 ? 'happy' : npcLook(g.i).face}}
					position={[g.p[0], g.p[1] + jump, g.p[2] - guestsUp * 0.6]}
					rotationY={Math.PI}
					pose={{time: t + n, sit: 1 - guestsUp, armsUp: cheer * 0.9, headPitch: -red * 0.5}}
				/>
			);
		})}
		<Avatar look={{...REQ_WED, face: reqFace}} position={R_POS} rotationY={Math.PI / 2} pose={{time: t, headPitch: -red * 0.55}} />
		<Avatar look={{...KLI_LOOK}} position={K_POS} rotationY={-Math.PI / 2} pose={{time: t, headPitch: -red * 0.4}} />
		{petals ? <Petals t={t} center={[0, 0, 8]} area={34} /> : null}
	</>
);

type WShot = {from: number; to: number; cam: (t: number, k: number) => Cam};
const WSHOTS: WShot[] = [
	{from: 64.5, to: 68.9, cam: (t, k) => ({pos: lerp3([0, 9, 42], [0, 6.5, 24], ease(k)), target: [0, 4.6, 0], fov: 50})},
	{from: 68.9, to: 73.2, cam: (t, k) => ({pos: lerp3([0, 5.4, 13], [0, 5.1, 11], ease(k)), target: [0, 4.5, 0], fov: 48})},
	{from: 73.2, to: 75.2, cam: (t, k) => ({pos: [2.2, 5.4, 6.2], target: [-2.4, 4.9, 0], fov: lerp(42, 36, ease(range(t, 73.2, 73.5)))})},
	{from: 75.2, to: 76.0, cam: () => ({pos: [-2.2, 5.4, 6.2], target: [2.4, 4.9, 0], fov: 38})},
	{from: 76.0, to: 77.5, cam: (t, k) => ({pos: lerp3([12, 13, 36], [10, 12, 32], k), target: [0, 3, 0], fov: 50})},
	{from: 77.5, to: 82.01, cam: (t, k) => ({pos: lerp3([-7.5, 4.2, 5.5], [-6.5, 3.6, 4.6], ease(k)), target: lerp3([1.5, 5.2, -1], [3, 9.5, -6], ease(range(t, 77.8, 79.2))), fov: 50})},
];

export const WeddingScene: React.FC<{t0: number}> = ({t0}) => {
	const frame = useCurrentFrame();
	const t = t0 + frame / FPS;
	const shot = WSHOTS.find((s) => t >= s.from && t < s.to) ?? WSHOTS[WSHOTS.length - 1];
	const k = clamp01((t - shot.from) / (shot.to - shot.from));
	const cam = shot.cam(t, k);
	const red = ease(range(t, 77.5, 80.0));
	const shk = shake(t, 0.04 * range(t, 77.4, 79) + 0.25 * range(t, 80.5, 82));
	cam.pos = [cam.pos[0] + shk[0], cam.pos[1] + shk[1], cam.pos[2] + shk[2]];
	const env: Env = {...lerpEnv(SUNSET_PINK, RED, red), shadowCenter: [0, 0, 6], shadowSize: 30};
	const cheer = t > 71.1 && t < 73.2 ? 1 : 0;
	const guestsUp = cheer ? 1 : red > 0.3 ? 1 : 0;
	const reqFace: Look['face'] = t < 70.5 ? 'happy' : t < 73.2 ? 'grin' : t < 77.5 ? 'grin' : 'worried';
	return (
		<AbsoluteFill>
			<Stage cam={cam} env={env}>
				<WeddingSet t={t} red={red} reqFace={reqFace} guestsUp={guestsUp} cheer={cheer} petals={red < 0.5} />
				<Meteor from={[-200, 160, -260]} to={[120, 40, -300]} k={range(t, 80.0, 81.6)} />
			</Stage>
			<Billboards
				cam={cam}
				t={t}
				items={[
					{p: R_POS, talking: reqTalking(t), hearts: t >= 70.7 ? t - 70.7 : undefined},
					{p: K_POS, name: 'lojjkli', bubble: bubbleFor(t), hearts: t >= 70.8 ? t - 70.8 : undefined},
					...GUESTS.filter((_, n) => n % 3 === 0).map((g) => ({p: [g.p[0], g.p[1] - 1 + guestsUp, g.p[2]] as V3, name: NPC_NAMES[g.i]})),
				]}
			/>
			<GameUI t={t} talking={reqTalking(t)} petsim={false} />
			{t > 71.0 && t < 73.2 ? (
				<div
					style={{
						position: 'absolute',
						left: 0,
						right: 0,
						top: 150,
						textAlign: 'center',
						fontFamily: '"Fredoka", "Noto Color Emoji", sans-serif',
						fontWeight: 700,
						fontSize: 96,
						color: '#ffd6ec',
						WebkitTextStroke: '12px #5a0b33',
						paintOrder: 'stroke fill',
						transform: `scale(${0.8 + 0.2 * Math.min(1, (t - 71.0) * 5)})`,
					}}
				>
					💍 JUST MARRIED 💍
				</div>
			) : null}
			<AlertBanner t={t} from={80.4} text="⚠️ SERVER ALERT: THE EARTH IS COLLAPSING ⚠️" />
		</AbsoluteFill>
	);
};
