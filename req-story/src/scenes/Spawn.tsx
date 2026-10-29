import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {Avatar, NPC_NAMES, npcLook, REQ_LOOK} from '../three/Avatar';
import {Cam, clamp01, ease, lerp3, V3} from '../three/cam';
import {Pet} from '../three/Props';
import {Clouds, DAY, Diamond, Fence, Flowers, Forest, Ground, Path, SpawnPad, Stage, CoinPile} from '../three/World';
import {DIAMONDS, FPS, reqTalking} from '../timeline';
import {Billboards} from '../ui/Billboards';
import {GameUI, ZoneBanner} from '../ui/HUD';

const WALK_START = 15.0;
const WALK_END = 21.0;
const SPEED = 6;

export const reqZ = (t: number) => -Math.min(Math.max(0, t - WALK_START), WALK_END - WALK_START) * SPEED;

const PICKUPS = DIAMONDS.filter(([at]) => at > 15 && at < 21).map(([at]) => at);

export const petFollow = (owner: V3, t: number, side: number, lag = 0.35): V3 => [owner[0] + side * 3.4, 0, owner[2] + 1.2 + Math.sin(t * 2 + side) * 0.3 + lag];

export const SpawnScene: React.FC<{t0: number}> = ({t0}) => {
	const frame = useCurrentFrame();
	const t = t0 + frame / FPS;
	const z = reqZ(t);
	const walking = t > WALK_START && t < WALK_END;
	const walkAmt = walking ? Math.min(1, (t - WALK_START) * 4, (WALK_END - t) * 4) : 0;
	// standing on the spawn pad until stepping off it
	const req: V3 = [0, z > -6 ? 0.5 : 0, z];
	const lookAround = t > WALK_END ? ease((t - WALK_END) / 0.8) : 0;
	const pz = reqZ(t - 0.35);
	const cam: Cam = {
		pos: lerp3([6, 9, req[2] + 18], [3, 7.5, req[2] + 14], ease((t - 14.5) / 3)),
		target: [req[0] - lookAround * 2, 4 + lookAround * 1.5, req[2] - 6],
		fov: 55,
	};
	cam.pos[0] += Math.sin(t * 0.7) * 0.6;
	const npcs: {p: V3; i: number; rot: number; wave?: boolean}[] = [
		{p: [-12, 0, -16], i: 0, rot: 0.6},
		{p: [10, 0, -22], i: 1, rot: -0.9, wave: true},
		{p: [-9, 0, -44], i: 2, rot: 0.2},
		{p: [14, 0, -40], i: 7, rot: -1.6},
	];
	return (
		<AbsoluteFill>
			<Stage cam={cam} env={{...DAY, shadowCenter: [0, 0, req[2] - 6], shadowSize: 45}}>
				<Ground />
				<SpawnPad />
				<Path from={[0, 0, -4]} to={[0, 0, -90]} width={10} />
				<Fence from={[-7, 0, -8]} to={[-7, 0, -60]} />
				<Fence from={[7, 0, -8]} to={[7, 0, -60]} />
				<Flowers center={[-16, 0, -30]} radius={7} seed={4} />
				<Flowers center={[18, 0, -12]} radius={6} seed={9} />
				<Forest count={46} radius={[26, 170]} seed={2} avoid={(x, zz) => Math.abs(x) < 20 && zz < 10 && zz > -95} />
				<Clouds t={t} />
				<CoinPile position={[-15, 0, -6]} />
				<CoinPile position={[16, 0, -30]} />
				{PICKUPS.map((at) =>
					t < at ? <Diamond key={at} position={[0, 0, -(at - WALK_START) * SPEED - 0.8]} t={t} /> : null,
				)}
				<Avatar
					look={REQ_LOOK}
					position={req}
					rotationY={Math.PI}
					pose={{walk: (t - WALK_START) * 9, walkAmt, time: t, headYaw: lookAround * 0.7}}
				/>
				<Pet kind="cat" position={petFollow([0, 0, pz], t, -1)} rotationY={Math.PI} t={t} />
				<Pet kind="dog" position={petFollow([0, 0, pz], t, 1)} rotationY={Math.PI} t={t + 1} />
				{npcs.map((n) => (
					<Avatar key={n.i} look={npcLook(n.i)} position={n.p} rotationY={n.rot} pose={{time: t + n.i, wave: n.wave && t > 17.6 && t < 19.6 ? 1 : 0}} />
				))}
			</Stage>
			<Billboards
				cam={cam}
				t={t}
				items={[
					{p: req, talking: reqTalking(t)},
					...npcs.map((n) => ({p: n.p, name: NPC_NAMES[n.i]})),
				]}
			/>
			<GameUI t={t} talking={reqTalking(t)} stick={walking ? [0, -walkAmt] : [0, 0]} />
			<ZoneBanner text="🌴 Spawn" t={t} from={14.9} />
			{/* quick fade in from loading screen */}
			<AbsoluteFill style={{background: '#000', opacity: 1 - clamp01((t - t0) / 0.4)}} />
		</AbsoluteFill>
	);
};
