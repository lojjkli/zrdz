import React from 'react';
import {KLI_DEEP, Look, npcLook, NPC_NAMES, REQ_LOOK} from '../three/Avatar';
import {Cam, ease, easeOut, range, V3} from '../three/cam';
import {FaceKind} from '../three/textures';
import {Arch, Bench, Petals} from '../three/Props';
import {Clouds, CoinPile, Forest} from '../three/World';
import {LOBBY_DAY, LOBBY_SUNSET} from '../three/MM2World';
import {M, T} from '../timeline';
import {Actor, Grass, HeartPuff, path, pick, SceneDef, Y} from './Engine';
import {face} from './shots';

const ss = (from: V3, to: V3, fov = 44) => (): Cam => ({pos: from, target: to, fov});
const drift = (from: V3, to: V3, target: V3, fov = 46, period = 8) => (t: number): Cam => {
	const k = (Math.sin(t / period) + 1) / 2;
	return {pos: [from[0] + (to[0] - from[0]) * k, from[1] + (to[1] - from[1]) * k, from[2] + (to[2] - from[2]) * k], target, fov};
};

const PIG_CU: [number, number] = [0.45, 4.2];

const TopHat: React.FC<{p: V3; yaw: number; s: number}> = ({p, yaw, s}) => (
	<group position={p} rotation={[0, yaw, 0]} scale={s}>
		<group position={[0, 0.7, 0.5]} rotation={[-0.15, 0, 0.15]}>
			<mesh>
				<cylinderGeometry args={[0.32, 0.32, 0.04, 16]} />
				<meshStandardMaterial color="#111" />
			</mesh>
			<mesh position={[0, 0.2, 0]}>
				<cylinderGeometry args={[0.2, 0.2, 0.4, 16]} />
				<meshStandardMaterial color="#111" />
			</mesh>
			<mesh position={[0, 0.06, 0]}>
				<cylinderGeometry args={[0.205, 0.205, 0.08, 16]} />
				<meshStandardMaterial color="#ff4f9a" />
			</mesh>
		</group>
	</group>
);

/** coins shooting out of the machine's screen like tears */
const CoinTears: React.FC<{t: number; from: number; at: V3; yaw?: number}> = ({t, from, at, yaw = 0}) => {
	if (t < from) return null;
	const k = Math.min(1, (t - from) / 0.6);
	return (
		<group position={at} rotation={[0, yaw, 0]}>
			{new Array(36).fill(0).map((_, i) => {
				const side = i % 2 ? 1 : -1;
				const ph = (t * 0.9 + i / 36) % 1;
				const x = side * (3.2 + ph * 5 + Math.sin(i) * 0.6);
				const y = 8.6 + ph * 5 - ph * ph * 14;
				if (y < 0.2) return null;
				return (
					<mesh key={i} position={[x, y, 2.6 + Math.cos(i * 3) * 0.8]} rotation={[t * 6 + i, i, 0]} scale={k}>
						<cylinderGeometry args={[0.35, 0.35, 0.08, 12]} />
						<meshStandardMaterial color="#ffcc33" metalness={0.8} roughness={0.25} emissive="#7a5500" emissiveIntensity={0.3} />
					</mesh>
				);
			})}
		</group>
	);
};

const REQ = (f: FaceKind): Look => ({...REQ_LOOK, face: f});

// ================================================================ the lobby (part 4)
const MACH: V3 = [0, 0, 0];
const REQ_L: V3 = [4.5, Y, 10];

const lobbyCast = (late: boolean): Actor[] => {
	const cast: Actor[] = [
		{id: 'mach', kind: 'machine', p: MACH, yaw: 0, x: (t) => ({lights: !late && t > T.mach_fine && t < T.mach_fine + 2.5 ? Math.abs(Math.sin(t * 20)) : 0})},
		{
			id: 'req',
			kind: 'avatar',
			look: REQ_LOOK,
			p: REQ_L,
			yaw: face(REQ_L, [0, 0, 2]),
			face: late
				? (t) => pick<FaceKind>(t, [[0, 'smile'], [T.n_week + 2.5, 'shock'], [T.mach_gentle, 'angry'], [T.kli_dumb, 'sad'], [T.req_back, 'angry']])
				: (t) => pick<FaceKind>(t, [[0, 'worried'], [T.req_bro, 'smile'], [T.mach_special, 'worried'], [T.req_notyou, 'sad'], [T.mach_fine, 'shock'], [T.req_mine, 'angry'], [T.n_cried, 'sad']]),
			pose: (t) => ({armsUp: (late && t > T.req_pigeon && t < T.req_pigeon + 1.2) || (!late && t > T.req_mine && t < T.req_mine + 1.3) ? 1 : 0, point: late && t > T.req_mything && t < T.req_mything + 2 ? 1 : 0, flex: late && t > T.req_back ? 1 : 0}),
		},
	];
	if (late) {
		cast.push(
			{id: 'pig', kind: 'pigeon', p: [4.2, 2.0 + 0.6 * 1.6, 2.6], s: 1.6, yaw: -0.2, cu: PIG_CU},
			{id: 'kli', kind: 'avatar', look: KLI_DEEP, p: [-7, Y, 13], yaw: face([-7, 0, 13], [0, 0, 4]), face: () => 'kli'},
			{id: 'ham', kind: 'hamster', p: [-3.8, Y, 14.5], s: 1.1, yaw: face([-3.8, 0, 14.5], [3, 0, 10]), x: () => ({shades: true})},
		);
	}
	return cast;
};

const lobbySet = (late: boolean) => (t: number) => (
	<>
		<Grass />
		<Clouds t={t} color={late ? '#ffd6e6' : '#ffffff'} />
		<Forest count={40} radius={[40, 140]} />
		{late ? (
			<>
				<TopHat p={[4.2, 2.0 + 0.6 * 1.6, 2.6]} yaw={-0.2} s={1.6} />
				<HeartPuff at={[2.5, 4, 3]} t={t} k={t > T.mach_gentle && t < T.mach_gentle + 3.2 ? 1 : 0} />
				<HeartPuff at={[-2, 10, 3]} t={t + 0.5} k={t > T.pig_coo + 0.4 && t < T.pig_coo + 2.4 ? 1 : 0} />
				<CoinPile position={[-6, 0, 5]} />
			</>
		) : (
			<>
				<CoinTears t={t} from={M.cry} at={MACH} />
				{t > M.cry + 1.5 ? (
					<>
						<CoinPile position={[-6, 0, 5]} />
						<CoinPile position={[6, 0, 5]} />
					</>
				) : null}
			</>
		)}
	</>
);

const reqLow = (t: number): Cam => ({pos: [REQ_L[0] - 2.2, 1.6, REQ_L[2] - 4.6], target: [REQ_L[0], 4.7, REQ_L[2]], fov: 44});

const LOBBY: SceneDef = {
	env: LOBBY_DAY,
	front: [0, 0, 30],
	wides: [drift([16, 8, 26], [13, 8, 24], [1, 5, 4]), drift([-13, 5, 22], [-11, 5, 21], [2, 5, 3], 48), ss([0, 7.5, 24], [0, 6.5, 0], 52)],
	cast: lobbyCast(false),
	set: lobbySet(false),
};

const LATER: SceneDef = {
	env: LOBBY_SUNSET,
	front: [0, 0, 30],
	wides: [drift([18, 9, 30], [15, 9, 28], [0, 4, 6], 48), drift([-14, 6, 26], [-12, 6, 25], [1, 5, 6], 48)],
	shots: {
		couple: (t, k) => ({pos: [0.8 - k * 0.5, 4.2, 11 - k], target: [2.6, 5.2, 2], fov: 50}),
		reqlow: reqLow,
	},
	cast: lobbyCast(true),
	set: lobbySet(true),
};

// ================================================================ the wedding (part 5)
const MACH_W: V3 = [-12.5, 0, -2];
const MACH_YAW = 0.35;
const PED: V3 = [6.5, 0, 0.5];
const PIG_W: V3 = [PED[0], 3 + 0.6 * 1.6, PED[2]];
const BREAD: V3 = [12.5, 0.05, 7];
const PIG_B: V3 = [11.3, 0.6 * 1.6, 7.4];
const REQ_IN: V3 = [0, Y, 5.5];

const pigPath = (t: number): V3 =>
	M.fly === undefined || t < M.fly + 0.2
		? PIG_W
		: (() => {
				const k = range(t, M.fly + 0.2, M.fly + 1.5);
				const p = [PIG_W[0] + (PIG_B[0] - PIG_W[0]) * ease(k), PIG_W[1] + (PIG_B[1] - PIG_W[1]) * k + Math.sin(k * Math.PI) * 3, PIG_W[2] + (PIG_B[2] - PIG_W[2]) * ease(k)] as V3;
				return p;
		  })();

const GUESTS: {p: V3; i: number}[] = (() => {
	const out: {p: V3; i: number}[] = [];
	[11, 15, 19].forEach((z, r) =>
		[-6.5, 6.5].forEach((x, c) =>
			[-2.4, 0, 2.4].forEach((dx, j) => {
				if (r === 0 && c === 0 && j === 2) return; // kli's seat
				out.push({p: [x + dx, Y, z], i: r * 6 + c * 3 + j});
			}),
		),
	);
	return out;
})();

const reelSpin = (t: number): [number, number, number] => {
	if (M.lever === undefined || t < M.lever + 0.2) return [0.4, 1.7, 3.1];
	return [0, 1, 2].map((i) => {
		const start = [0.4, 1.7, 3.1][i];
		const end = M.lever + 2.6 + i * 0.7;
		return start + (3 + 6 * 5 - start) * easeOut(range(t, M.lever + 0.2, end));
	}) as [number, number, number];
};

const weddingCast = (post: boolean): Actor[] => {
	if (post)
		return [
			{id: 'ham', kind: 'hamster', p: [0, 2.0, -1.2], s: 1.2, yaw: 0, x: () => ({hat: true})},
			{id: 'pig', kind: 'pigeon', p: (t) => [-1.1, 0.4 + 0.6 * 1.3 + (t > M.peck + 1.1 ? Math.abs(Math.sin((t - M.peck) * 9)) * 0.6 : 0), 3], s: 1.3, yaw: 0.9, cu: PIG_CU},
			{id: 'bread', kind: 'bread', p: [1.1, 0.4, 3], s: 1.5, yaw: -0.9, name: 'The Bread'},
		];
	return [
		{id: 'mach', kind: 'machine', p: MACH_W, yaw: MACH_YAW, x: (t) => ({spin: reelSpin(t), lights: M.lever !== undefined && t > M.lever + 4.1 && t < M.lever + 6.5 ? Math.abs(Math.sin(t * 16)) * 1.5 : 0})},
		{id: 'ham', kind: 'hamster', p: [0, 2.0, -1.2], s: 1.2, yaw: 0, x: (t) => ({hat: true, jump: t > T.req_object && t < T.req_object + 0.5 ? 0.6 : 0})},
		{id: 'pig', kind: 'pigeon', p: pigPath, s: 1.6, yaw: (t) => (M.fly !== undefined && t > M.fly + 0.2 ? face(PIG_W, PIG_B) : -0.3), cu: PIG_CU, x: (t) => ({flap: M.fly !== undefined && t > M.fly + 0.2 && t < M.fly + 1.5 ? 1 : 0})},
		{
			id: 'req',
			kind: 'avatar',
			look: REQ_LOOK,
			p: (t) => path(t, [[0, [0, Y, 34]], [M.object, REQ_IN]], 0.7),
			yaw: Math.PI,
			face: (t) => pick<FaceKind>(t, [[0, 'angry'], [T.mach_last, 'hearts'], [T.n_dogs, 'shock'], [T.req_lost, 'sad'], [T.mach_bread, 'shock'], [T.req_friends, 'worried'], [T.req_no, 'angry'], [T.n_end, 'grin']]),
			pose: (t) => ({walk: t * 14, walkAmt: t > M.object - 0.7 && t < M.object ? 1 : 0, point: t > T.req_object && t < T.req_object + 1 ? 1 : 0, armsUp: t > T.req_spin && t < T.req_spin + 3.5 ? 1 : 0, cover: t > T.req_lost && t < T.req_lost + 1.6 ? 1 : 0}),
		},
		{id: 'kli', kind: 'avatar', look: KLI_DEEP, p: [-4.1, Y, 11], yaw: Math.PI, face: (t) => (t > T.req_spin + 2.2 ? 'klishock' : 'kli'), pose: () => ({sit: 1}), cu: [3.3, 6.5]},
		{id: 'bread', kind: 'bread', p: (t) => [BREAD[0], BREAD[1] + Math.max(0, 9 * (1 - easeOut(range(t, M.bread, M.bread + 0.8)))), BREAD[2]], s: 1.6, yaw: -0.6, name: null, show: (t) => M.bread !== undefined && t > M.bread},
		...GUESTS.map(
			(g): Actor => ({
				id: 'crowd',
				kind: 'avatar',
				look: npcLook(g.i),
				p: g.p,
				yaw: Math.PI,
				name: g.i % 4 === 1 ? NPC_NAMES[g.i % NPC_NAMES.length] : null,
				face: (t) => (t > T.req_object && t < T.mach_last ? 'shock' : t > T.n_dogs && t < T.mach_sign + 2 ? 'worried' : 'happy'),
				pose: (t) => ({sit: 1, armsUp: t > T.crowd_gasp && t < T.crowd_gasp + 1.2 ? 1 : 0, headYaw: t > T.req_object - 0.2 && t < T.req_spin ? Math.sign(g.p[0]) * -0.6 : 0}),
			}),
		),
	];
};

const weddingSet = (post: boolean) => (t: number) => (
	<>
		<Grass color="#6bbf4a" />
		<Clouds t={t} />
		<Forest count={40} radius={[40, 140]} />
		<Arch position={[0, 0, 0]} />
		<Petals t={t} center={[0, 0, 8]} count={60} area={30} />
		<mesh position={[0, 1.0, -1.4]} castShadow>
			<boxGeometry args={[1.8, 2, 1.3]} />
			<meshStandardMaterial color="#8a5a33" />
		</mesh>
		<mesh position={[0, 0.03, 14]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
			<planeGeometry args={[3, 22]} />
			<meshStandardMaterial color="#c8102e" roughness={0.8} />
		</mesh>
		{post ? <TopHat p={[-1.1, 0.4 + 0.6 * 1.3 + (t > M.peck + 1.1 ? Math.abs(Math.sin((t - M.peck) * 9)) * 0.6 : 0), 3]} yaw={0.9} s={1.3} /> : null}
		{post ? (
			<group position={[1.1, 0.4, 3]} rotation={[0, -0.9, 0]} scale={1.5}>
				<mesh position={[0, 0.78, 0]}>
					<coneGeometry args={[0.32, 0.55, 16, 1, true]} />
					<meshStandardMaterial color="#ffffff" transparent opacity={0.75} side={2} />
				</mesh>
			</group>
		) : (
			<>
				<mesh position={[PED[0], 1.5, PED[2]]} castShadow>
					<cylinderGeometry args={[0.9, 1.1, 3, 16]} />
					<meshStandardMaterial color="#f4f1ea" />
				</mesh>
				{[11, 15, 19].map((z) => [-6.5, 6.5].map((x) => <Bench key={x + '_' + z} position={[x, 0, z + 0.45]} rotationY={Math.PI} />))}
				<TopHat p={pigPath(t)} yaw={M.fly !== undefined && t > M.fly + 0.2 ? face(PIG_W, PIG_B) : -0.3} s={1.6} />
				<HeartPuff at={[-6, 9, 1]} t={t} k={t > T.mach_last && t < T.n_lever ? 1 : 0} />
			</>
		)}
	</>
);

const SCREEN: V3 = [MACH_W[0] + Math.sin(MACH_YAW) * 2.2, 8.6, MACH_W[2] + Math.cos(MACH_YAW) * 2.2];

const WEDDING: SceneDef = {
	env: {...LOBBY_DAY, sunIntensity: 2.6},
	front: [0, 0, 30],
	wides: [drift([7, 9, 32], [4, 9, 31], [0, 5, 2], 48), drift([-2, 8, 26], [1, 8, 25], [-4, 6, 0], 54), ss([16, 6, 18], [0, 4, 6], 50)],
	shots: {
		burst: (t, k) => ({pos: [1.4, 4.8, -0.4], target: [0, 4.2, 9 - k * 3], fov: 46}),
		reels: (t, k) => ({pos: [SCREEN[0] + Math.sin(MACH_YAW) * (10 - k), 8.9, SCREEN[2] + Math.cos(MACH_YAW) * (10 - k)], target: SCREEN, fov: 40}),
		breadcam: () => ({pos: [16.5, 3.4, 15], target: [12.5, 1.0, 7], fov: 42}),
		flight: (t) => {
			const p = pigPath(t);
			return {pos: [p[0] + 1, p[1] + 3, p[2] + 13], target: [p[0], p[1] + 0.4, p[2]], fov: 46};
		},
	},
	cast: weddingCast(false),
	set: weddingSet(false),
};

const POST: SceneDef = {
	env: {...LOBBY_SUNSET, hemiIntensity: 1.3},
	front: [0, 0, 30],
	wides: [drift([0, 3.6, 12], [1, 3.4, 11], [0, 1.6, 2], 40)],
	cast: weddingCast(true),
	set: weddingSet(true),
};

export const SCENE_DEFS: Record<string, SceneDef> = {lobby: LOBBY, later: LATER, wedding: WEDDING, post: POST};
