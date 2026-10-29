import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {Avatar, KLI_DEEP, KLI_RICH, MYNINN_LOOK, npcLook} from '../three/Avatar';
import {Cam, ease, lerp, lerp3, range, V3} from '../three/cam';
import {Sparkles, Spotlight} from '../three/Props';
import {Clouds, Stage} from '../three/World';
import {LOBBY_DAY} from '../three/MM2World';
import {baseplateTexture, CashRain, Car, Donut, GoldMansion, RollingDonut, ViewportGrid} from '../three/KliProps';
import {FPS, HATERS, talking} from '../timeline';
import {Billboards, BB} from '../ui/Billboards';
import {DOC_FONT, UI_FONT} from '../ui/HUD';
import {DisconnectDialog} from '../ui/Dialogs';
import {BigText, GameUI} from '../ui/MM2';
import {BlenderUI, Fade, RobuxCounter} from '../ui/KliUI';
import {Grain, Letterbox, Vignette} from './Doc';
import {VOID} from './Early';
import {face, Shot, shotAt, withShake} from './shots';

const Grass: React.FC = () => (
	<mesh position={[0, -0.5, 0]} receiveShadow>
		<boxGeometry args={[400, 1, 400]} />
		<meshStandardMaterial map={baseplateTexture('richgrass', '#4f9a3a', '#468a33', 100)} roughness={0.9} />
	</mesh>
);

const KLI_AT: V3 = [0, 0, 0];
const MANSION: V3 = [0, 0, -32];
const CAR: V3 = [7, 0, -14];
const MY_AT: V3 = [3.6, 0, 1];
const HATER_X = [-4.5, -1.5, 1.5, 4.5];
const haterPos = (i: number, t: number): V3 => {
	const z = lerp(26, 7.5, range(t, 136.4, 138.2));
	const away = Math.max(0, t - 141.6) * 6;
	return [HATER_X[i], 0, z + away];
};
const robux = (t: number) => Math.round(999_999_999 * ease(range(t, 129.4, 135)) ** 2);

// giant donut #1 rolls along +x behind kli and flattens the car
const donutX = (t: number) => (t < 159 ? -90 + 96 * Math.max(0, (t - 156) / 3) ** 2 : 6 + (t - 159) * 64);
// giant donut #2 rolls straight at the camera
const donut2Z = (t: number) => lerp(-60, 30, range(t, 162.4, 163.25));
const DONUT_R = 13;

const RICH_SHOTS: Shot[] = [
	{from: 126, to: 129, cam: (t, k) => ({pos: lerp3([6.2, 5.0, 6.2], [5.4, 4.6, 5.6], k), target: [0, 1, 0], fov: 40})},
	{from: 129, to: 133.6, cam: (t, k) => ({pos: lerp3([22, 7, 30], [14, 10, 26], ease(k)), target: [0, 8, -12], fov: 50})},
	{from: 133.6, to: 136.4, cam: (t, k) => ({pos: lerp3([1.8, 5.2, 8.5], [1.5, 5.0, 7.6], k), target: [0, 4.6, 0], fov: 46})},
	{from: 136.4, to: 139.8, cam: (t, k) => ({pos: lerp3([-2.2, 6.8, -7], [-2.0, 6.6, -6.2], k), target: [0, 4, 9], fov: 50})},
	{from: 139.8, to: 141.4, cam: () => ({pos: [0.9, 4.0, 4.2], target: [0, 5.0, 0], fov: 46})},
	{from: 141.4, to: 146, cam: (t, k) => {
		const a = lerp(-0.5, 0.4, k);
		return {pos: [Math.sin(a) * 34, 16, Math.cos(a) * 34], target: [0, 6, -12], fov: 46};
	}},
	{from: 146, to: 152, cam: (t, k) => ({pos: lerp3([1.8, 5.2, 11.5], [1.8, 5.0, 10.4], k), target: [1.8, 4.4, 0], fov: 44})},
];

const DONUT_SHOTS: Shot[] = [
	{from: 152, to: 154.6, cam: (t, k) => ({pos: lerp3([1.8, 5.0, 10.4], [1.6, 4.9, 9.4], k), target: [1.8, 4.4, 0], fov: 44})},
	{from: 154.6, to: 157.6, cam: (t, k) => ({pos: lerp3([24, 9, 28], [22, 9, 26], k), target: [-30, 10, -14], fov: 50})},
	{from: 157.6, to: 161, cam: (t, k) => ({pos: [26, 6, 10], target: lerp3([-10, 8, -14], [20, 8, -14], range(t, 157.6, 160)), fov: 54})},
	{from: 161, to: 162.4, cam: (t, k) => ({pos: [0.5, 4.7, 4.6], target: [0, 4.6, 0], fov: 44})},
	{from: 162.4, to: 168, cam: () => ({pos: [0, 6, 20], target: [0, 8, 0], fov: 52})},
];

export const RichScene: React.FC<{t0: number; mode: 'rich' | 'donut'}> = ({t0, mode}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const rich = mode === 'rich';
	const shake = rich ? (t > 139.8 && t < 140.4 ? 0.06 : 0) : t > 157.6 && t < 163.2 ? 0.08 + (t > 159 && t < 159.6 ? 0.2 : 0) : 0;
	const cam: Cam = withShake(shotAt(rich ? RICH_SHOTS : DONUT_SHOTS, t).cam, t, shake);
	const app = rich && t < 129;
	const kTalk = talking('kli', t);
	const haters = rich && t >= 136.4 && t < 145;
	const myOn = !rich || t >= 145.8;
	const myPop = rich ? Math.min(1, Math.max(0, (t - 145.8) / 0.2)) : 1;
	const d1x = donutX(t);
	const carSquash = !rich && t > 159 ? 1 : 0;
	const d2z = donut2Z(t);
	const kliCrushed = !rich && d2z > -4;
	const black = !rich && t >= 163.2;
	const runners = !rich && t > 157.6;
	const bbs: BB[] = [];
	if (!app && !kliCrushed) bbs.push({p: KLI_AT, name: 'lojjkli', talking: kTalk});
	if (!app && myOn && !kliCrushed) bbs.push({p: MY_AT, name: 'myninn', talking: talking('myninn', t)});
	if (haters) HATERS.forEach((h, i) => bbs.push({p: haterPos(i, t), name: h.name}));
	return (
		<AbsoluteFill style={{background: '#000'}}>
			{!black ? (
				<Stage cam={cam} env={app ? {...LOBBY_DAY, skyTop: '#3d3d3d', skyHorizon: '#3d3d3d', skyBottom: '#3d3d3d', fog: ['#3d3d3d', 400, 900], sunGlow: 0} : {...LOBBY_DAY, shadowCenter: [0, 0, -8], shadowSize: 40}}>
					{app ? (
						<>
							<ViewportGrid />
							<Donut position={[0, 1.2, 0]} rotation={[0.35, t * 0.9, 0]} scale={1.7} />
						</>
					) : (
						<>
							<Grass />
							<Clouds t={t} />
							<GoldMansion position={MANSION} />
							<Car position={CAR} rotationY={-0.5} squash={carSquash} />
							{rich ? <CashRain t={t} center={[0, 0, -4]} k={range(t, 129.2, 131)} area={46} /> : null}
							{!kliCrushed ? (
								<Avatar
									look={KLI_RICH}
									position={KLI_AT}
									rotationY={rich && t >= 139.8 && t < 141.4 ? -0.5 : 0}
									pose={{time: t, flex: rich && t >= 133.6 && t < 136.4 ? 1 : 0, wave: rich && t >= 148.2 && t < 150 ? 1 : 0, headYaw: rich && t >= 139.8 && t < 141.4 ? -0.4 : 0}}
								/>
							) : null}
							{myOn && !kliCrushed ? <Avatar look={MYNINN_LOOK} position={MY_AT} rotationY={face(MY_AT, [0, 0, 8])} scale={myPop} pose={{time: t + 1, point: rich && t > 146 && t < 147.8 ? 1 : 0}} /> : null}
							{haters
								? HATERS.map((h, i) => {
										const p = haterPos(i, t);
										const leaving = t > 141.6;
										return (
											<Avatar
												key={h.name}
												look={{...npcLook([3, 8, 10, 5][i]), face: t > 139.8 ? 'sad' : 'happy'}}
												position={p}
												rotationY={leaving ? 0 : Math.PI}
												pose={{time: t + i, walk: t * 10, walkAmt: t < 138.2 || leaving ? 1 : 0, armsUp: t > 137.8 && t < 139.6 ? 0.5 : 0}}
											/>
										);
								  })
								: null}
							{!rich ? (
								<>
									{t >= 154.6 && t < 162 ? <RollingDonut position={[d1x, DONUT_R, -14]} yaw={Math.PI / 2} roll={(d1x + 90) / DONUT_R} scale={9} /> : null}
									{t >= 162.4 ? <RollingDonut position={[0, DONUT_R, d2z]} roll={(d2z + 60) / DONUT_R} scale={9} /> : null}
									{runners
										? [0, 1, 2].map((i) => (
												<Avatar
													key={i}
													look={{...npcLook(20 + i), face: 'scream'}}
													position={[14 + i * 3 + (t - 157.6) * 7, 0, -6 + i * 2.5]}
													rotationY={Math.PI / 2}
													pose={{time: t, walk: t * 14, walkAmt: 1, armsUp: 1}}
												/>
										  ))
										: null}
								</>
							) : null}
						</>
					)}
				</Stage>
			) : null}
			{app ? (
				<BlenderUI t={t} outliner={['Camera', 'Light', 'Donut']} title="donut_final_FINAL.blend" />
			) : !black ? (
				<>
					<Billboards cam={cam} t={t} items={bbs} />
					<GameUI t={t} talking={kTalk} mode="plain" chatFrom={136} />
					<RobuxCounter value={rich ? robux(t) : 999_999_999} gold pulse={rich && t > 129.4 && t < 135 ? Math.abs(Math.sin(t * 14)) * 0.25 : 0} />
				</>
			) : null}
			{rich ? (
				<>
					<BigText t={t} from={127.4} to={128.9} text="🍩 DONUT: COMPLETE" color="#ff9ad5" top={130} />
					<BigText t={t} from={139.85} to={141.3} text="NAH." color="#fff" top={150} size={150} />
					<BigText t={t} from={142.0} to={145.8} text="#1 RICHEST DEV 👑" color="#ffd84d" top={140} />
				</>
			) : (
				<>
					<BigText t={t} from={155.4} to={157.4} text="⚠️ PHYSICS: ON" color="#ff5b5b" top={140} />
					{t >= 163.8 ? <DisconnectDialog t={t - 163.8} message="The donut has eaten the server." code="404 DONUT" /> : null}
				</>
			)}
			<Fade t={t} inAt={t0} inDur={rich ? 0.4 : 0.01} outFrom={rich ? 999 : 167.4} outTo={rich ? 1000 : 168} />
		</AbsoluteFill>
	);
};

// ================================================================ end card + post-credit
export const KliEndCard: React.FC<{t0: number}> = ({t0}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const lt = t - t0;
	const fadeOut = range(t, 173.6, 174.2);
	const by = range(t, 169.6, 170.2);
	const soon = range(t, 170.2, 170.8);
	const post = t > 174.4;
	const pt = t - 174.4;
	const kliCam: Cam = withShake(
		{pos: lerp3([0, 5.0, 7.0], [0, 5.0, 5.4], ease(range(t, 174.4, 179))), target: [0, 4.9, 0], fov: 38},
		t,
		t > 177.2 && t < 178 ? 0.06 * (1 - (t - 177.2) / 0.8) : 0,
	);
	const kFace = t > 176.1 && t < 177.2 ? 'klishock' : 'kli';
	return (
		<AbsoluteFill style={{background: '#000'}}>
			{!post ? (
				<AbsoluteFill style={{opacity: 1 - fadeOut}}>
					<div style={{position: 'absolute', left: 0, right: 0, top: 250, display: 'flex', justifyContent: 'center', gap: 40}}>
						{['K', 'L', 'I'].map((l, i) => {
							const k = ease(range(lt, 0.2 + i * 0.25, 0.6 + i * 0.25));
							return (
								<div key={l} style={{fontFamily: DOC_FONT, fontSize: 320, lineHeight: 1, color: '#fff', opacity: k, transform: `translateY(${(1 - k) * -80}px) scale(${1.3 - 0.3 * k})`, textShadow: '0 0 50px rgba(143,123,255,0.6)'}}>
									{l}
								</div>
							);
						})}
					</div>
					<div style={{position: 'absolute', left: '50%', top: 590, width: 560 * ease(range(lt, 1.0, 1.6)), height: 5, background: '#8f7bff', transform: 'translateX(-50%)'}} />
					<div style={{position: 'absolute', left: 0, right: 0, top: 620, textAlign: 'center', fontFamily: UI_FONT, fontSize: 38, letterSpacing: 14, color: '#cfcfcf', opacity: by, fontWeight: 600}}>
						A STORY BY LOJJKLI
					</div>
					<div style={{position: 'absolute', left: 0, right: 0, top: 700, textAlign: 'center', fontFamily: DOC_FONT, fontSize: 110, letterSpacing: 18, color: '#b9a8ff', opacity: soon, transform: `scale(${1.08 - 0.08 * soon})`}}>
						COMING SOON
					</div>
				</AbsoluteFill>
			) : (
				<AbsoluteFill style={{opacity: interpolate(pt, [0, 0.3, 5.0, 5.6], [0, 1, 1, 0], {extrapolateRight: 'clamp'})}}>
					<Stage cam={kliCam} env={VOID}>
						<Spotlight position={[2, 10, 6]} target={[0, 4.5, 0]} intensity={700} color="#c9b8ff" />
						<pointLight position={[-3, 5, 3]} color="#7b5cff" intensity={20} distance={12} />
						<Avatar look={{...KLI_DEEP, face: kFace}} position={[0, 0, 0]} pose={{time: t}} />
					</Stage>
					<Vignette amt={0.9} />
				</AbsoluteFill>
			)}
			<Grain t={t} opacity={0.06} />
			<Letterbox />
		</AbsoluteFill>
	);
};
