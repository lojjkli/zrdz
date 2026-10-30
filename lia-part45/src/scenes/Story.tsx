import React from 'react';
import {ADE_LOOK, LIA_LOOK, Look} from '../three/Avatar';
import {Cam, ease, easeOut, range, V3} from '../three/cam';
import {FaceKind} from '../three/textures';
import {Clouds} from '../three/World';
import {DutchFlag, LOBBY_DAY, LOBBY_NIGHT, LOBBY_SUNSET, Tulips} from '../three/MM2World';
import {baseplateTexture} from '../three/KliProps';
import {M, T} from '../timeline';
import {Actor, HeartPuff, path, pick, SceneDef, Y} from './Engine';
import {face} from './shots';

const ss = (from: V3, to: V3, fov = 44) => (): Cam => ({pos: from, target: to, fov});
const drift = (from: V3, to: V3, target: V3, fov = 46, period = 8) => (t: number): Cam => {
	const k = (Math.sin(t / period) + 1) / 2;
	return {pos: [from[0] + (to[0] - from[0]) * k, from[1] + (to[1] - from[1]) * k, from[2] + (to[2] - from[2]) * k], target, fov};
};

export const ADE: Look = {...ADE_LOOK, hat: undefined, hair: 'long', hairColor: '#2a1a12', bow: '#ffeb3b', face: 'lia'};
export const DAVID: Look = {head: '#ffdcc2', torso: '#e85d3a', arms: '#e85d3a', legs: '#2b2d31', face: 'smile', shirt: 'stripe', shirtColor: '#ffd166', hat: 'backcap', hatColor: '#1e88e5'};
const PIG_CU: [number, number] = [0.45, 4.2];

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

const Field: React.FC<{t: number; mill?: boolean}> = ({t}) => (
	<>
		<Grass />
		<Clouds t={t} />
		<House />
		<Tulips center={[-19, 0, 2]} w={12} d={8} rows={6} />
		<DutchFlag position={[-10, 0, -6]} t={t} />
	</>
);

const Crater: React.FC<{p: V3; k: number}> = ({p, k}) =>
	k <= 0 ? null : (
		<mesh position={[p[0], 0.06, p[2]]} rotation={[-Math.PI / 2, 0, 0]} scale={k}>
			<circleGeometry args={[3, 24]} />
			<meshStandardMaterial color="#5a3d22" roughness={1} />
		</mesh>
	);

const Wind: React.FC<{t: number; k: number}> = ({t, k}) =>
	k <= 0 ? null : (
		<>
			{new Array(26).fill(0).map((_, i) => {
				const ph = (t * 1.4 + i / 26) % 1;
				return (
					<mesh key={i} position={[-6 + ph * 50, 1 + ((i * 7) % 11), -2 + ((i * 5) % 14)]} scale={[k, 1, 1]}>
						<boxGeometry args={[4, 0.06, 0.06]} />
						<meshBasicMaterial color="#ffffff" transparent opacity={0.7 * (1 - ph)} />
					</mesh>
				);
			})}
		</>
	);

// ================================================================ part 4: Lia's house
const LIA_P: V3 = [-2.6, Y, 0];
const ADE_P: V3 = [2.6, Y, 0.6];
const KIDS_P: V3 = [20, 0, -2];
const kidsYaw = face([KIDS_P[0] - 4, 0, KIDS_P[2] + 4], [0, 0, 2]);

const kidsCam = (): Cam => ({pos: [8, 6, 12], target: [19, 2, 0], fov: 48});

const HOME: SceneDef = {
	env: LOBBY_DAY,
	front: [0, 0, 24],
	wides: [drift([0, 7, 22], [3, 7, 21], [0, 4, 0], 48), drift([-14, 5, 16], [-12, 5, 15], [2, 4, 0], 48)],
	shots: {kidscam: kidsCam},
	cast: [
		{id: 'lia', kind: 'avatar', look: LIA_LOOK, p: LIA_P, face: (t) => pick<FaceKind>(t, [[0, 'lia'], [M.adein, 'liashock'], [T.ade_why + 2.6, 'liasad'], [T.ade_twice, 'liashock']]), pose: (t) => ({wave: t < T.lia_normal + 2 && t > T.lia_normal ? 1 : 0})},
		{
			id: 'ade',
			kind: 'avatar',
			look: ADE,
			p: (t) => path(t, [[0, [18, Y, 6]], [M.adein, ADE_P]], 1.2),
			yaw: (t) => (t < M.adein ? face([18, 0, 6], ADE_P) : face(ADE_P, [0, 0, 24])),
			face: (t) => pick<FaceKind>(t, [[0, 'liacry'], [T.ade_twice, 'angry']]),
			pose: (t) => ({walk: t * 16, walkAmt: t > M.adein - 1.2 && t < M.adein ? 1 : 0, armsUp: (t > M.adein && t < M.adein + 1.6) || (t > T.ade_twice && t < T.ade_twice + 2) ? 1 : 0, cover: t > T.ade_why && t < T.ade_why + 2 ? 1 : 0}),
		},
		{id: 'kids', kind: 'kids', p: KIDS_P, yaw: kidsYaw, x: (t) => ({armsUp: t > T.kids_gasp && t < T.kids_gasp + 1.5 ? 1 : 0})},
	],
	set: (t) => <Field t={t} />,
};

const MILL_FAR: V3 = [-26, 0, -40];
const HOME2: SceneDef = {
	...HOME,
	shots: {kidscam: kidsCam, millfar: (t, k) => ({pos: [-8 - k, 9, -10], target: [-26, 14, -40], fov: 40})},
	cast: [
		{id: 'lia', kind: 'avatar', look: LIA_LOOK, p: LIA_P, face: (t) => pick<FaceKind>(t, [[0, 'liasad'], [T.ade_moving, 'lia'], [T.ade_mill + 1, 'liashock'], [T.lia_therapist, 'angry']]), pose: (t) => ({armsUp: t > T.lia_therapist && t < T.lia_therapist + 2 ? 1 : 0})},
		{id: 'ade', kind: 'avatar', look: ADE, p: ADE_P, face: (t) => pick<FaceKind>(t, [[0, 'liasad'], [T.ade_moving, 'lia'], [T.ade_mill, 'hearts']])},
		{id: 'donut', kind: 'donut', p: [-6.4, Y, 2], s: 1.1, x: () => ({mood: 'smug', bowtie: true})},
		{id: 'mill', kind: 'mill', p: MILL_FAR, s: 2.0, yaw: face(MILL_FAR, [0, 0, 0]), x: (t) => ({mood: t > T.ade_mill ? 'love' : 'happy'})},
		{id: 'kids', kind: 'kids', p: KIDS_P, yaw: kidsYaw},
	],
};

// ================================================================ part 4: David under the windmill
const MILL_P: V3 = [0, 0, -8];
const DAV_M: V3 = [6, Y, 3];
const PIG_FROM: V3 = [16, 12, 14];
const PIG_HEAD: V3 = [DAV_M[0], 4.95 + 0.6 * 1.1, DAV_M[2]];

const MILL: SceneDef = {
	env: {...LOBBY_SUNSET, hemiIntensity: 1.5, sunDir: [0.4, 0.7, 0.8]},
	front: [0, 0, 24],
	wides: [drift([14, 8, 22], [12, 8, 20], [0, 6, -2], 50)],
	shots: {davhead: (t, k) => ({pos: [DAV_M[0] + 2.4, 6.4, DAV_M[2] + 9.5 - k], target: [DAV_M[0], 5.2, DAV_M[2]], fov: 42})},
	cast: [
		{id: 'mill', kind: 'mill', p: MILL_P, s: 1.6, yaw: 0, x: () => ({mood: 'happy'})},
		{
			id: 'dav',
			kind: 'avatar',
			look: DAVID,
			p: DAV_M,
			face: (t) => pick<FaceKind>(t, [[0, 'sad'], [T.dav_prove, 'angry'], [T.pig_coo + 0.4, 'shock'], [T.dav_aah, 'scream']]),
			pose: (t) => ({cover: t < T.dav_cry + 3 ? 1 : 0, point: t > T.dav_prove && t < T.dav_prove + 1 ? 1 : 0, armsUp: t > T.dav_aah ? 1 : 0, jump: t > T.dav_aah ? Math.abs(Math.sin(t * 12)) * 0.6 : 0}),
		},
		{
			id: 'pig',
			kind: 'pigeon',
			p: (t) => {
				const k = range(t, M.pigland - 1.2, M.pigland);
				const base: V3 = [PIG_FROM[0] + (PIG_HEAD[0] - PIG_FROM[0]) * ease(k), PIG_FROM[1] + (PIG_HEAD[1] - PIG_FROM[1]) * easeOut(k), PIG_FROM[2] + (PIG_HEAD[2] - PIG_FROM[2]) * ease(k)];
				const hop = t > T.dav_aah ? Math.abs(Math.sin(t * 12)) * 0.6 : 0;
				return [base[0], base[1] + hop, base[2]];
			},
			s: 1.1,
			yaw: 0.3,
			cu: PIG_CU,
			show: (t) => t > M.pigland - 1.3,
			x: (t) => ({flap: t < M.pigland ? 1 : 0}),
		},
	],
	set: (t) => (
		<>
			<Grass />
			<Clouds t={t} color="#ffd6e6" />
			<Tulips center={[-12, 0, 4]} w={12} d={8} rows={6} />
			<Tulips center={[14, 0, -4]} w={10} d={8} rows={5} />
		</>
	),
};

// ================================================================ part 5: the plan
const PLAN: SceneDef = {
	env: {...LOBBY_SUNSET, hemiIntensity: 1.2},
	front: [0, 0, 24],
	wides: [drift([0, 7, 22], [3, 7, 21], [0, 4, 0], 48)],
	cast: [
		{id: 'lia', kind: 'avatar', look: LIA_LOOK, p: LIA_P, face: (t) => pick<FaceKind>(t, [[0, 'lia'], [T.dav_three + 0.5, 'liasad']]), pose: (t) => ({point: t > T.lia_steps && t < T.lia_steps + 3 ? 0.6 : 0})},
		{id: 'dav', kind: 'avatar', look: DAVID, p: ADE_P, face: (t) => pick<FaceKind>(t, [[0, 'sad'], [T.dav_three, 'grin']]), pose: (t) => ({flex: t > T.dav_three && t < T.dav_three + 1.6 ? 1 : 0})},
	],
	set: (t) => <Field t={t} />,
};

// ================================================================ part 5: the date
const DMILL: V3 = [0, 0, -9];
const ADE_D: V3 = [-2.6, Y, 1.5];
const DAV_IN: V3 = [7.5, Y, 5];
const davFly = (t: number): V3 => {
	if (M.sing === undefined || t < M.sing - 1.4) return [22, Y, 9];
	if (t < M.blow) return path(t, [[0, [22, Y, 9]], [M.sing, DAV_IN]], 1.4);
	const k = range(t, M.blow, M.blow + 3.2);
	return [DAV_IN[0] + k * 50, Y + k * 22 + Math.sin(k * Math.PI) * 6, DAV_IN[2] + k * 10];
};

const DATE: SceneDef = {
	env: {...LOBBY_DAY, sunIntensity: 2.4},
	front: [0, 0, 24],
	wides: [drift([-14, 7, 20], [-12, 7, 19], [1, 6, -2], 50), ss([4, 6, 26], [3, 6, -2], 54)],
	shots: {
		blow: (t) => {
			const p = davFly(t);
			return {pos: [p[0] - 10, p[1] + 4, p[2] + 16], target: [p[0], p[1] + 3, p[2]], fov: 50};
		},
	},
	cast: [
		{
			id: 'mill',
			kind: 'mill',
			p: DMILL,
			s: 1.6,
			yaw: 0,
			x: (t) => ({
				mood: t > T.mill_sad - 0.3 ? 'sad' : t > T.dav_sing && t < T.ade_cute ? 'angry' : 'love',
				spin: t * 1.2 + (M.cringe === undefined ? 0 : Math.pow(Math.min(5, Math.max(0, t - M.cringe)), 2) * 3),
			}),
		},
		{
			id: 'ade',
			kind: 'avatar',
			look: ADE,
			p: ADE_D,
			yaw: (t) => (t > T.dav_sing - 0.4 && t < T.ade_sorry ? face(ADE_D, DAV_IN) : face(ADE_D, [0, 0, 24])),
			face: (t) => pick<FaceKind>(t, [[0, 'hearts'], [T.dav_sing, 'liashock'], [T.ade_cute, 'hearts'], [T.ade_sorry, 'liasad']]),
			pose: () => ({sit: 1}),
			cu: [3.2, 6.8],
		},
		{
			id: 'dav',
			kind: 'avatar',
			look: DAVID,
			p: davFly,
			yaw: (t) => (t < M.sing ? face([22, 0, 9], DAV_IN) : face(DAV_IN, ADE_D)),
			face: (t) => pick<FaceKind>(t, [[0, 'grin'], [M.blow, 'scream'], [T.dav_worth, 'hearts']]),
			pose: (t) => ({walk: t * 14, walkAmt: t < M.sing ? 1 : 0, point: t > M.sing && t < M.blow ? 1 : 0, fly: t > M.blow ? 1 : 0, wave: t > T.dav_worth ? 1 : 0}),
			show: (t) => M.sing !== undefined && t > M.sing - 1.4 && t < M.blow + 3.4,
		},
	],
	set: (t) => (
		<>
			<Grass />
			<Clouds t={t} />
			<Tulips center={[-14, 0, 6]} w={14} d={10} rows={7} />
			<Tulips center={[14, 0, -2]} w={14} d={10} rows={7} />
			<mesh position={[-2.6, 0.06, 1.5]} rotation={[-Math.PI / 2, 0, 0]}>
				<planeGeometry args={[5, 4]} />
				<meshStandardMaterial color="#e63946" />
			</mesh>
			<HeartPuff at={[-1.5, 6, 0]} t={t} k={t > T.mill_tulip && t < T.dav_sing ? 1 : 0} />
			<Wind t={t} k={M.cringe !== undefined && t > M.cringe + 2 && t < M.blow + 3 ? 1 : 0} />
		</>
	),
};

// ================================================================ part 5: crash landing
const DAV_L: V3 = [2.4, Y, 2];
const ADE_L: V3 = [-1.4, Y, 2.6];
const LAND: SceneDef = {
	env: {...LOBBY_SUNSET, hemiIntensity: 1.2},
	front: [0, 0, 24],
	wides: [drift([0, 8, 24], [4, 8, 23], [3, 3, 0], 54)],
	shots: {
		kidscam: kidsCam,
		crash: (t) => ({pos: [-6, 4, 16], target: [DAV_L[0], 3, DAV_L[2]], fov: 50}),
	},
	cast: [
		{id: 'lia', kind: 'avatar', look: LIA_LOOK, p: [-6, Y, -0.5], face: (t) => pick<FaceKind>(t, [[0, 'liashock'], [T.ade_real, 'lia'], [T.lia_onenormal, 'liacry']]), pose: (t) => ({armsUp: t > T.lia_onenormal && t < T.lia_onenormal + 2 ? 1 : 0})},
		{
			id: 'dav',
			kind: 'avatar',
			look: DAVID,
			p: (t) => (M.land === undefined || t > M.land + 0.9 ? DAV_L : [DAV_L[0] + 30 * (1 - range(t, M.land - 0.1, M.land + 0.9)), Y + 30 * (1 - range(t, M.land - 0.1, M.land + 0.9)), DAV_L[2]]),
			yaw: face(DAV_L, [-1, 0, 14]),
			side: 1,
			face: (t) => pick<FaceKind>(t, [[0, 'scream'], [M.land + 0.9, 'sick'], [T.dav_real, 'hearts']]),
			pose: (t) => ({fly: t < M.land + 0.9 ? 1 : 0, armsUp: t > T.crowd_no ? 1 : 0}),
		},
		{
			id: 'ade',
			kind: 'avatar',
			look: ADE,
			p: (t) => path(t, [[0, [-16, Y, 8]], [T.ade_real - 0.4, ADE_L]], 1.4),
			yaw: (t) => (t < T.ade_real - 0.4 ? face([-16, 0, 8], ADE_L) : face(ADE_L, [1.5, 0, 14])),
			side: -1,
			face: (t) => pick<FaceKind>(t, [[0, 'liashock'], [T.dav_real, 'hearts']]),
			pose: (t) => ({walk: t * 16, walkAmt: t > T.ade_real - 1.8 && t < T.ade_real - 0.4 ? 1 : 0, armsUp: t > T.crowd_no ? 1 : 0}),
		},
		{id: 'kids', kind: 'kids', p: KIDS_P, yaw: kidsYaw, x: (t) => ({jump: t > T.kids_aww && t < T.kids_aww + 2 ? 0.8 : 0, armsUp: t > T.crowd_no ? 1 : 0})},
	],
	set: (t) => (
		<>
			<Field t={t} />
			<Crater p={DAV_L} k={M.land !== undefined && t > M.land + 0.9 ? 1 : 0} />
			<HeartPuff at={[0.5, 6, 2.3]} t={t} k={t > T.dav_real + 0.6 ? 1 : 0} />
		</>
	),
};

// ================================================================ post credits: two exes
const PM: V3 = [-9, 0, -6];
const PS: V3 = [10, 0, -5];
const POST: SceneDef = {
	env: {...LOBBY_NIGHT, hemiIntensity: 1.1, sunIntensity: 1.4},
	front: [0, 0, 24],
	wides: [drift([0, 10, 34], [3, 10, 33], [0, 8, -4], 54)],
	cast: [
		{id: 'mill', kind: 'mill', p: PM, s: 1.4, yaw: face(PM, [4, 0, 14]), x: () => ({mood: 'love'})},
		{id: 'mach', kind: 'machine', p: PS, yaw: face(PS, [-4, 0, 14])},
	],
	set: (t) => (
		<>
			<Grass />
			<Tulips center={[0, 0, 8]} w={20} d={6} rows={4} />
			<HeartPuff at={[0, 10, 0]} t={t} k={t > T.mach_free ? 2 : 0} />
		</>
	),
};

export const SCENE_DEFS: Record<string, SceneDef> = {home: HOME, home2: HOME2, mill: MILL, plan: PLAN, date: DATE, land: LAND, post: POST};
