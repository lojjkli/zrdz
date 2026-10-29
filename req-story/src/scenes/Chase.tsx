import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {Avatar, KLI_LOOK, NPC_NAMES, npcLook} from '../three/Avatar';
import {Cam, range, shake, V3} from '../three/cam';
import {Arch, CollapseGround, Meteor, Pet} from '../three/Props';
import {Env, Stage, Tree} from '../three/World';
import {FPS, reqTalking} from '../timeline';
import {Billboards} from '../ui/Billboards';
import {GameUI} from '../ui/HUD';
import {AlertBanner} from '../ui/Dialogs';
import {RED, REQ_WED} from './Love';

const T0 = 82.0;
const RUN = 11;
const FRONT_Z0 = -30;
const FRONT_V = 13;
export const IMPACT = 88.6;

const frontZ = (t: number) => FRONT_Z0 + FRONT_V * (t - T0);

type Runner = {i: number; x: number; z0: number; v: number; trip?: number};
const RUNNERS: Runner[] = [
	{i: 0, x: -7, z0: -2, v: 11.4},
	{i: 1, x: 6.5, z0: 1, v: 11.2},
	{i: 2, x: -12, z0: -7, v: 11.8},
	{i: 3, x: 11, z0: -5, v: 11.6},
	{i: 4, x: -3.8, z0: -10, v: 12.0},
	{i: 5, x: 15, z0: -12, v: 12.3},
	{i: 6, x: -16, z0: -14, v: 12.4},
	{i: 7, x: 3.6, z0: -6, v: 7.8, trip: 1}, // bacon_hair2012 doesn't make it (oof)
];

const runnerPos = (r: Runner, t: number): V3 => {
	const dt = Math.max(0, t - T0);
	const z = r.z0 + r.v * dt;
	let y = 0;
	if (r.trip) {
		// falls once the collapse front reaches them
		const caught = T0 + (r.z0 - FRONT_Z0) / (FRONT_V - r.v) + 0.5;
		if (t > caught) y = -0.5 * 22 * (t - caught) ** 2;
	}
	return [r.x + Math.sin(t * 2 + r.i) * 0.6, y, z];
};

export const ChaseScene: React.FC<{t0: number; freezeAt?: number}> = ({t0, freezeAt}) => {
	const frame = useCurrentFrame();
	const t = freezeAt ?? t0 + frame / FPS;
	const dt = t - T0;
	const req: V3 = [0, 0, RUN * dt];
	const kli: V3 = [3.4, 2.2 + Math.sin(t * 5) * 0.4, RUN * dt - 1.2];
	const lookBack = range(t, 85.3, 85.6) - range(t, 86.7, 87.0);
	const shk = shake(t, 0.18 + 0.5 * Math.max(0, 1 - (t - T0) * 1.5) + 0.6 * range(t, 88.0, IMPACT));
	const cam: Cam = {
		pos: [2.2 + Math.sin(t * 0.9) * 1.2 + shk[0], 12 + shk[1], req[2] + 20],
		target: [0, 0, req[2] - 26],
		fov: 58,
		roll: Math.sin(t * 0.8) * 0.04 + shk[2] * 0.2,
	};
	const env: Env = {...RED, shadowCenter: [0, 0, req[2] - 10], shadowSize: 40};
	// pets get left behind at the edge of the collapse
	const petFall = (delay: number): V3 => {
		const zf = frontZ(85.0) + 5;
		const k = Math.max(0, t - 85.15 - delay);
		return [delay ? 4 : -4, -0.5 * 20 * k * k, zf];
	};
	const archFall = Math.max(0, t - (T0 + (-40 - FRONT_Z0) / FRONT_V + 0.3));
	return (
		<AbsoluteFill>
			<Stage cam={cam} env={env}>
				<CollapseGround t={t} t0={T0} z0={FRONT_Z0} v={FRONT_V} />
				<group position={[0, -0.5 * 22 * archFall * archFall, -40]} rotation={[-archFall * 0.4, 0, archFall * 0.2]}>
					<Arch />
				</group>
				{[[-24, -20], [26, -6], [-30, 14], [22, 30], [-20, 46]].map(([x, z], n) => {
					const k = Math.max(0, t - (T0 + (z - FRONT_Z0) / FRONT_V + 0.6));
					return <Tree key={n} position={[x, -0.5 * 22 * k * k, z]} seed={n} />;
				})}
				<Avatar look={{...REQ_WED, face: 'scream'}} position={req} rotationY={0} pose={{walk: t * 15, walkAmt: 1, time: t, armsUp: 0.25, headYaw: lookBack * Math.PI * 0.9, lean: 0.12}} />
				<Avatar look={KLI_LOOK} position={kli} rotationY={0} pose={{fly: 0.55, time: t}} />
				{RUNNERS.map((r) => (
					<Avatar
						key={r.i}
						look={{...npcLook(r.i), face: 'scream'}}
						position={runnerPos(r, t)}
						rotationY={0}
						pose={{walk: t * 15 + r.i, walkAmt: 1, armsUp: 0.9, time: t + r.i, lean: 0.1}}
					/>
				))}
				{t > 84.8 ? (
					<>
						<Pet kind="cat" position={petFall(0)} rotationY={0} t={t} />
						<Pet kind="dog" position={petFall(0.2)} rotationY={0} t={t + 1} />
					</>
				) : null}
				<Meteor from={[110, 150, -140]} to={[34, 0, -50]} k={range(t, 84.6, 85.4)} />
				<Meteor from={[-120, 160, -90]} to={[-40, 0, -6]} k={range(t, 86.2, 87.0)} />
				<Meteor from={[24, 70, RUN * (IMPACT - T0) - 170]} to={[2.2, 12, RUN * (IMPACT - T0) + 20]} k={range(t, 87.4, IMPACT)} />
			</Stage>
			<Billboards
				cam={cam}
				t={t}
				items={[
					{p: req, talking: reqTalking(t)},
					{p: kli, name: 'lojjkli'},
					...RUNNERS.map((r) => ({p: runnerPos(r, t), name: NPC_NAMES[r.i]})),
				]}
			/>
			<GameUI t={t} talking={reqTalking(t)} stick={[0.1, 1]} jump={Math.sin(t * 4) > 0.85} petsim={false} />
			<AlertBanner t={t} from={80.4} text="⚠️ SERVER ALERT: THE EARTH IS COLLAPSING ⚠️" />
			{/* boom flash at the start, white-out on impact */}
			<AbsoluteFill style={{background: '#fff', opacity: Math.max(0, 1 - dt * 3) * 0.9}} />
			<AbsoluteFill style={{background: '#fff', opacity: range(t, IMPACT - 0.15, IMPACT)}} />
		</AbsoluteFill>
	);
};
