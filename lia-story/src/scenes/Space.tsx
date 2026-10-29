import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {Cam, ease, lerp3, range} from '../three/cam';
import {Stage} from '../three/World';
import {Planet, SPACE} from '../three/MM2World';
import {FPS} from '../timeline';
import {DisconnectDialog} from '../ui/Dialogs';
import {RoleReveal} from '../ui/MM2';
import {withShake} from './shots';

export const BOOM = 124.4;

const PlanetShot: React.FC<{t: number}> = ({t}) => {
	const k = t < BOOM ? 0 : Math.pow((t - BOOM) / 2.4, 0.7);
	const base: Cam = {pos: lerp3([0, 12, 84], [0, 8, 70], ease(range(t, 123.6, 127.4))), target: [0, 0, 0], fov: 42};
	const cam = withShake(base, t, t > BOOM ? 1.6 * Math.max(0, 1 - (t - BOOM) / 2.2) : 0);
	return (
		<AbsoluteFill style={{background: '#000'}}>
			<Stage cam={cam} env={SPACE}>
				<Planet k={k} t={t} />
				{/* the green cloud spreading over the planet just before it pops */}
				{t < BOOM ? (
					<mesh scale={23 + range(t, 123.6, BOOM) * 1.5}>
						<icosahedronGeometry args={[1, 3]} />
						<meshBasicMaterial color="#8fdc2a" transparent opacity={0.15 + range(t, 123.6, BOOM) * 0.45} depthWrite={false} />
					</mesh>
				) : null}
			</Stage>
		</AbsoluteFill>
	);
};

export const SpaceScene: React.FC<{t0: number}> = ({t0}) => {
	const t = t0 + useCurrentFrame() / FPS;
	return (
		<AbsoluteFill>
			<PlanetShot t={t} />
			<AbsoluteFill style={{background: '#fff', opacity: Math.max(1 - range(t, t0, t0 + 0.35), t > BOOM ? 1 - range(t, BOOM, BOOM + 0.6) : 0)}} />
		</AbsoluteFill>
	);
};

export const DisconnectScene: React.FC<{t0: number}> = ({t0}) => {
	const t = t0 + useCurrentFrame() / FPS;
	return (
		<AbsoluteFill style={{background: '#000'}}>
			<AbsoluteFill style={{filter: 'blur(6px) brightness(0.5) saturate(0.7)'}}>
				<PlanetShot t={126.8} />
			</AbsoluteFill>
			<DisconnectDialog t={t - t0 - 0.2} message="The experience's server has exploded." code="67" />
			<AbsoluteFill style={{background: '#000', opacity: interpolate(t, [t0, t0 + 0.2, 131.0, 131.4], [1, 0, 0, 1], {extrapolateRight: 'clamp'})}} />
		</AbsoluteFill>
	);
};

export const RoleScene: React.FC<{t0: number}> = ({t0}) => {
	const t = t0 + useCurrentFrame() / FPS;
	return <RoleReveal t={t - t0} />;
};
