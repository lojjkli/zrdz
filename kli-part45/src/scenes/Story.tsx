import React from 'react';
import {KLI_DEEP, KLI_RICH} from '../three/Avatar';
import {Cam, ease, range, V3} from '../three/cam';
import {FaceKind} from '../three/textures';
import {Rain} from '../three/Props';
import {Clouds, Forest} from '../three/World';
import {INDOOR, LobbyBench, LOBBY_DAY, LOBBY_NIGHT, LOBBY_SUNSET} from '../three/MM2World';
import {Car, CashRain, GoldChair, GoldMansion} from '../three/KliProps';
import {M, T} from '../timeline';
import {Actor, Floor, Grass, HeartPuff, Juice, path, pick, SceneDef, Y} from './Engine';
import {face} from './shots';

const ss = (from: V3, to: V3, fov = 44) => (): Cam => ({pos: from, target: to, fov});
const drift = (from: V3, to: V3, target: V3, fov = 46, period = 8) => (t: number): Cam => {
	const k = (Math.sin(t / period) + 1) / 2;
	return {pos: [from[0] + (to[0] - from[0]) * k, from[1] + (to[1] - from[1]) * k, from[2] + (to[2] - from[2]) * k], target, fov};
};
const PIG_CU: [number, number] = [0.45, 4.2];
const DONUT_S = 1.3;

const Stool: React.FC<{p: V3; h?: number}> = ({p, h = 1.5}) => (
	<group position={p}>
		<mesh position={[0, h - 0.1, 0]} castShadow>
			<cylinderGeometry args={[0.8, 0.8, 0.2, 16]} />
			<meshStandardMaterial color="#c0392b" />
		</mesh>
		<mesh position={[0, (h - 0.2) / 2, 0]}>
			<cylinderGeometry args={[0.12, 0.12, h - 0.2, 8]} />
			<meshStandardMaterial color="#ccc" metalness={0.6} />
		</mesh>
	</group>
);

const Table: React.FC<{p: V3; w?: number}> = ({p, w = 6}) => (
	<group position={p}>
		<mesh position={[0, 1.9, 0]} castShadow receiveShadow>
			<boxGeometry args={[w, 0.25, 2.2]} />
			<meshStandardMaterial color="#8a5a33" />
		</mesh>
		<mesh position={[0, 0.95, 0.9]} castShadow>
			<boxGeometry args={[w, 1.9, 0.15]} />
			<meshStandardMaterial color="#6d4426" />
		</mesh>
	</group>
);

// ================================================================ part 4: the mansion
const KLI_M: V3 = [-3.2, Y, 0];
const DON_M: V3 = [3, Y, 0.6];
const BAG_M: V3 = [7.4, Y, 1.6];
const GONE: V3 = [30, Y, 12];

const MANSION: SceneDef = {
	env: LOBBY_DAY,
	front: [0, 0, 24],
	wides: [drift([0, 7, 22], [3, 7, 21], [0, 4, -2], 50), drift([-14, 5, 16], [-12, 5, 15], [1, 4, -2], 48)],
	cast: [
		{id: 'kli', kind: 'avatar', look: KLI_RICH, p: KLI_M, face: (t) => pick<FaceKind>(t, [[0, 'kli'], [T.donut_leaving + 1.4, 'klishock'], [T.donut_cousin, 'kliwide'], [T.kli_once + 1, 'klisad']]), pose: (t) => ({armsUp: t > T.kli_bagel && t < T.kli_bagel + 1.2 ? 1 : 0, point: t > T.kli_gave && t < T.kli_gave + 3 ? 0.7 : 0})},
		{
			id: 'donut',
			kind: 'donut',
			p: (t) => path(t, [[0, DON_M], [M.leave + 2.4, GONE]], 1.6),
			s: DONUT_S,
			yaw: (t) => (t > M.leave + 0.8 ? face(DON_M, GONE) : face(DON_M, [0, 0, 24])),
			x: (t) => ({bowtie: true, mood: t > T.bagel_hi ? 'happy' : 'smug', wobble: t > M.leave + 0.8 ? 1 : 0}),
		},
		{
			id: 'bagel',
			kind: 'bagel',
			p: (t) => path(t, [[0, [24, Y, 6]], [M.bagelin, BAG_M], [M.leave + 2.4, [GONE[0] + 3, Y, GONE[2]]]], 1.6),
			yaw: (t) => (t < M.bagelin || t > M.leave + 0.8 ? -Math.PI / 2 + (t > M.leave ? Math.PI : 0) : face(BAG_M, [0, 0, 24])),
			s: 1.2,
			show: (t) => M.bagelin !== undefined && t > M.bagelin - 1.8,
		},
	],
	set: (t) => (
		<>
			<Grass />
			<Clouds t={t} />
			<GoldMansion position={[0, 0, -32]} />
			<Car position={[-14, 0, -6]} rotationY={0.6} />
			<Forest count={30} radius={[50, 140]} />
			<HeartPuff at={[6, 4, 1.5]} t={t} k={t > T.bagel_hi + 0.6 ? 1 : 0} />
		</>
	),
};

// ================================================================ part 4: court
const JUDGE: V3 = [0, 2.05, -6.2];
const KLI_C: V3 = [-5, Y, 3];
const DON_C: V3 = [5, Y, 3];
const PIG_C0: V3 = [0, 0.96, 4];
const PIG_C1: V3 = [1.8, 2.05 + 0.96, -5.6];

const Courtroom: React.FC = () => (
	<>
		<Floor color="#8a6240" size={60} />
		<mesh position={[0, 8, -12]} receiveShadow>
			<boxGeometry args={[40, 16, 1]} />
			<meshStandardMaterial color="#d8c3a0" />
		</mesh>
		{[-20, 20].map((x) => (
			<mesh key={x} position={[x, 8, 4]} receiveShadow>
				<boxGeometry args={[1, 16, 34]} />
				<meshStandardMaterial color="#cdb690" />
			</mesh>
		))}
		<mesh position={[0, 1.0, -6]} castShadow receiveShadow>
			<boxGeometry args={[8, 2, 2.4]} />
			<meshStandardMaterial color="#5a3a22" />
		</mesh>
		<mesh position={[0, 9, -11.4]}>
			<circleGeometry args={[2.2, 32]} />
			<meshStandardMaterial color="#e8b423" metalness={0.7} roughness={0.3} />
		</mesh>
		{[-5, 5].map((x) => (
			<mesh key={x} position={[x, 1.1, 1.4]} castShadow>
				<boxGeometry args={[3.6, 2.2, 1]} />
				<meshStandardMaterial color="#6d4426" />
			</mesh>
		))}
	</>
);

const COURT: SceneDef = {
	env: {...INDOOR, hemiIntensity: 1.3, sunIntensity: 2},
	front: [0, 0, 24],
	wides: [ss([0, 7, 20], [0, 4, -3], 52), drift([12, 6, 14], [10, 6, 13], [0, 3, -2], 50)],
	shots: {
		pigcam: (t) => ({pos: [6, 5, 10], target: [0.8, 1.6, -1], fov: 50}),
	},
	cast: [
		{id: 'cube', kind: 'cube', p: JUDGE, s: 1.3, yaw: 0, x: () => ({wig: true}), cu: [1.4, 7]},
		{id: 'kli', kind: 'avatar', look: KLI_RICH, p: KLI_C, yaw: face(KLI_C, [0, 0, 0]), side: 1, face: (t) => pick<FaceKind>(t, [[0, 'kli'], [T.kli_ohno, 'klishock'], [T.kli_me, 'kli'], [T.cube_mine + 1.5, 'klishock'], [T.kli_lost, 'klisad']]), pose: (t) => ({armsUp: t > T.kli_me && t < T.kli_me + 1 ? 1 : 0})},
		{id: 'donut', kind: 'donut', p: DON_C, s: DONUT_S, yaw: face(DON_C, [0, 0, 0]), side: -1, x: (t) => ({bowtie: true, mood: t > T.cube_mine + 1.5 ? 'hurt' : 'smug'})},
		{
			id: 'pig',
			kind: 'pigeon',
			p: (t) => {
				const k = range(t, M.pigwalk + 0.4, M.pigwalk + 1.6);
				return [PIG_C0[0] + (PIG_C1[0] - PIG_C0[0]) * ease(k), PIG_C0[1] + (PIG_C1[1] - PIG_C0[1]) * ease(k) + Math.sin(k * Math.PI) * 2, PIG_C0[2] + (PIG_C1[2] - PIG_C0[2]) * ease(k)] as V3;
			},
			s: 1.6,
			yaw: (t) => (t < M.pigwalk + 0.4 ? 0 : t < M.pigwalk + 1.6 ? Math.PI : 0),
			cu: PIG_CU,
			x: (t) => ({flap: t > M.pigwalk + 0.4 && t < M.pigwalk + 1.6 ? 1 : 0}),
		},
	],
	set: () => <Courtroom />,
};

// ================================================================ part 5: rain
const RAIN: SceneDef = {
	env: {...LOBBY_NIGHT, hemiIntensity: 1.8, sunIntensity: 1.6},
	front: [0, 0, 24],
	wides: [drift([6, 5, 14], [4, 5, 13], [0, 3, 0], 50)],
	cast: [{id: 'kli', kind: 'avatar', look: KLI_DEEP, p: [0, Y, 0.2], yaw: 0, face: () => 'klisad', pose: (t) => ({sit: 1, headPitch: 0.25}), cu: [3.4, 7]}],
	set: (t) => (
		<>
			<Grass />
			<LobbyBench position={[0, 0, -0.4]} />
			<Rain t={t} center={[0, 0, 4]} count={500} area={30} />
			<pointLight position={[0, 9, 6]} color="#b8ccff" intensity={160} distance={30} />
		</>
	),
};

// ================================================================ part 5: auditions (and the comeback)
const KLI_A: V3 = [0, Y, -2.4];
const SPOT: V3 = [0, Y, 5];
const STOOL: V3 = [0, 0, 5];

const AudSet: React.FC<{t: number}> = ({t}) => (
	<>
		<Grass />
		<Clouds t={t} />
		<Forest count={30} radius={[40, 140]} />
		<Table p={[0, 0, -1.4]} />
		<mesh position={[0, 4.6, -4.5]}>
			<boxGeometry args={[9, 1.8, 0.2]} />
			<meshStandardMaterial color="#ffd166" />
		</mesh>
	</>
);

const AUD: SceneDef = {
	env: LOBBY_DAY,
	front: [0, 0, 24],
	wides: [drift([9, 7, 16], [7, 7, 15], [0, 3, 1], 50)],
	shots: {breadcam: (t, k) => ({pos: [0.8, 3.2, 1.0 + k * 0.6], target: [0, 1.8, 5], fov: 40})},
	cast: [
		{id: 'kli', kind: 'avatar', look: KLI_DEEP, p: KLI_A, yaw: 0, face: (t) => pick<FaceKind>(t, [[0, 'klisad'], [T.kli_hired, 'kli']]), pose: (t) => ({point: t > T.kli_hired && t < T.kli_hired + 1.4 ? 1 : 0})},
		{id: 'ham', kind: 'hamster', p: (t) => path(t, [[0, SPOT], [M.next + 1.6, [-16, Y, 10]]], 1.2), s: 1.2, yaw: (t) => (t > M.next ? -Math.PI / 2 : Math.PI), x: () => ({shades: true}), show: (t) => t < M.next + 1.6, side: 1, cu: [1.1, 3.4]},
		{id: 'bread', kind: 'bread', p: [STOOL[0], 1.5, STOOL[2]], s: 1.6, yaw: Math.PI * 0.9, name: 'Bread', show: (t) => t > M.breadin, cu: [0.5, 3.4]},
	],
	set: (t) => (
		<>
			<AudSet t={t} />
			{t > M.breadin ? <Stool p={STOOL} /> : null}
			{t < M.next + 1.6 ? <Juice position={[1.2, 0, 5.4]} /> : null}
		</>
	),
};

const KLI_B: V3 = [-2.8, Y, 0.4];
const DON_B: V3 = [3.2, Y, 1];
const BREAD_B: V3 = [0, 1.5, 0.8];
const PIG_SKY: V3 = [14, 12, 10];
const PIG_EAT: V3 = [0.2, 1.5 + 0.96, 0.8];
const BACK: SceneDef = {
	env: {...LOBBY_SUNSET, hemiIntensity: 1.3},
	front: [0, 0, 24],
	wides: [drift([0, 6, 18], [2, 6, 17], [0, 3, 0], 48)],
	shots: {eatcam: (t) => ({pos: [1.6, 4.2, 9.5], target: [0.2, 2.2, 0.8], fov: 46})},
	cast: [
		{id: 'kli', kind: 'avatar', look: KLI_DEEP, p: KLI_B, yaw: face(KLI_B, [2, 0, 20]), face: (t) => pick<FaceKind>(t, [[0, 'kli'], [M.eat + 2.6, 'klishock'], [T.kli_welcome, 'kli']]), pose: (t) => ({armsUp: t > M.hug ? 1 : 0})},
		{id: 'bread', kind: 'bread', p: BREAD_B, s: 1.6, yaw: 0.2, name: 'Bread', show: (t) => !(M.eat !== undefined && t > M.eat + 2.6), cu: [0.5, 3.4]},
		{id: 'donut', kind: 'donut', p: (t) => path(t, [[0, DON_B], [M.hug + 0.6, [-0.4, Y, 1.4]]], 0.6), s: DONUT_S, yaw: (t) => face(DON_B, [-2, 0, 20]), x: (t) => ({bowtie: true, mood: t > T.kli_welcome ? 'happy' : 'hurt', tears: t < T.kli_welcome ? 1 : 0, wobble: t > M.hug ? 1 : 0})},
		{
			id: 'pig',
			kind: 'pigeon',
			p: (t) => {
				const k = range(t, M.eat + 0.6, M.eat + 2.2);
				return [PIG_SKY[0] + (PIG_EAT[0] - PIG_SKY[0]) * ease(k), PIG_SKY[1] + (PIG_EAT[1] - PIG_SKY[1]) * ease(k), PIG_SKY[2] + (PIG_EAT[2] - PIG_SKY[2]) * ease(k)] as V3;
			},
			s: 1.3,
			yaw: -0.4,
			cu: PIG_CU,
			show: (t) => M.eat !== undefined && t > M.eat + 0.5,
			x: (t) => ({flap: t < M.eat + 2.2 ? 1 : 0}),
		},
	],
	set: (t) => (
		<>
			<AudSet t={t} />
			<Stool p={[0, 0, 0.8]} />
			<HeartPuff at={[-1.6, 5, 1]} t={t} k={t > M.hug ? 1.5 : 0} />
		</>
	),
};

// ================================================================ part 5: the date
const DON_D: V3 = [-2.2, Y, 0];
const BAG_D: V3 = [2.2, Y, 0];
const DATE: SceneDef = {
	env: LOBBY_SUNSET,
	front: [0, 0, 24],
	wides: [drift([0, 4.5, 14], [1.5, 4.5, 13], [0, 1.6, 0], 46)],
	shots: {reveal: (t) => ({pos: [3.0, 2.8, 7.4], target: [BAG_D[0], 1.4, 0], fov: 44})},
	cast: [
		{id: 'donut', kind: 'donut', p: DON_D, s: DONUT_S, yaw: face(DON_D, [2, 0, 12]), x: (t) => ({bowtie: true, mood: t > M.pop ? 'hurt' : 'happy', tears: t > T.donut_bird ? 1 : 0, wobble: t > T.donut_bird ? 1 : 0})},
		{id: 'bagel', kind: 'bagel', p: BAG_D, s: 1.2, yaw: face(BAG_D, [-2, 0, 12]), x: (t) => ({open: M.pop === undefined ? 0 : ease(range(t, M.pop, M.pop + 0.3))})},
		{id: 'pig', kind: 'pigeon', p: [BAG_D[0], 0.96, BAG_D[2] + 0.2], s: 1.6, yaw: face(BAG_D, [-2, 0, 12]), cu: PIG_CU, show: (t) => M.pop !== undefined && t > M.pop},
	],
	set: (t) => (
		<>
			<Grass />
			<Clouds t={t} color="#ffd6e6" />
			<Forest count={30} radius={[40, 140]} />
			<mesh position={[0, 0.06, 0.5]} rotation={[-Math.PI / 2, 0, 0]}>
				<planeGeometry args={[9, 5]} />
				<meshStandardMaterial color="#e63946" />
			</mesh>
			<HeartPuff at={[0, 3.5, 0]} t={t} k={t < M.pop ? 1 : 0} />
		</>
	),
};

// ================================================================ post credits: the cube keeps the mansion
const POST: SceneDef = {
	env: LOBBY_DAY,
	front: [0, 0, 24],
	wides: [drift([0, 5, 15], [2, 5, 14], [0, 2.4, 0], 46)],
	cast: [
		{id: 'cube', kind: 'cube', p: [0, 1.2, 0.2], s: 1.0, yaw: 0, x: () => ({wig: true})},
		{id: 'pig', kind: 'pigeon', p: [2.6, 0.96, 1], s: 1.6, yaw: -0.3, cu: PIG_CU},
	],
	set: (t) => (
		<>
			<Grass />
			<Clouds t={t} />
			<GoldMansion position={[0, 0, -32]} />
			<GoldChair position={[0, 0, 0]} />
			<CashRain t={t} center={[0, 0, 0]} count={120} area={20} />
		</>
	),
};

export const SCENE_DEFS: Record<string, SceneDef> = {mansion: MANSION, court: COURT, rain: RAIN, aud: AUD, date: DATE, back: BACK, post: POST};
