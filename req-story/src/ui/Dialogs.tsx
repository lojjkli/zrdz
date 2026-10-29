import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {DiamondIcon, RobuxIcon, UI_FONT} from './HUD';

const pop = (k: number) => (k < 0.18 ? 0.85 + (k / 0.18) * 0.15 : 1);

export const PurchasePrompt: React.FC<{t: number; from: number; buyAt: number; to: number}> = ({t, from, buyAt, to}) => {
	if (t < from || t > to) return null;
	const k = t - from;
	const o = interpolate(t, [from, from + 0.15, to - 0.15, to], [0, 1, 1, 0]);
	const bought = t >= buyAt + 0.12;
	const pressed = t >= buyAt - 0.1 && t < buyAt + 0.12;
	return (
		<AbsoluteFill style={{background: `rgba(0,0,0,${0.45 * o})`}}>
			<div
				style={{
					position: 'absolute',
					left: 960 - 380,
					top: 300,
					width: 760,
					height: 480,
					borderRadius: 22,
					background: '#232527',
					boxShadow: '0 20px 60px rgba(0,0,0,0.6)',
					opacity: o,
					transform: `scale(${pop(k)})`,
					fontFamily: UI_FONT,
					color: '#fff',
					overflow: 'hidden',
				}}
			>
				<div style={{height: 84, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 36, fontWeight: 800, borderBottom: '1px solid #3a3d42', position: 'relative'}}>
					{bought ? 'Purchase Completed' : 'Buy Item'}
					<div style={{position: 'absolute', right: 30, top: 22, fontSize: 32, color: '#bbb'}}>✕</div>
				</div>
				{bought ? (
					<div style={{padding: '50px 50px', fontSize: 32, textAlign: 'center', lineHeight: 1.4, fontWeight: 600}}>
						You have successfully bought
						<br />
						<b>Mega Diamond Pack</b>.
					</div>
				) : (
					<div style={{display: 'flex', gap: 34, padding: '30px 50px 0'}}>
						<div
							style={{
								width: 150,
								height: 150,
								borderRadius: 18,
								background: 'radial-gradient(circle,#2f5f9a,#0f2440)',
								display: 'flex',
								alignItems: 'center',
								justifyContent: 'center',
							}}
						>
							<DiamondIcon size={110} />
						</div>
						<div>
							<div style={{fontSize: 38, fontWeight: 800}}>Mega Diamond Pack</div>
							<div style={{fontSize: 26, color: '#a8abb2', marginTop: 4}}>250,000 Diamonds</div>
							<div style={{display: 'flex', alignItems: 'center', gap: 10, fontSize: 40, fontWeight: 800, marginTop: 18}}>
								<RobuxIcon size={36} /> 1,699
							</div>
						</div>
					</div>
				)}
				{!bought ? (
					<>
						<div style={{position: 'absolute', left: 50, right: 50, bottom: 136, fontSize: 24, color: '#a8abb2'}}>
							Your balance after this transaction will be <RobuxIcon size={20} color="#a8abb2" /> 0
						</div>
						<div style={{position: 'absolute', left: 50, right: 50, bottom: 36, display: 'flex', gap: 24}}>
							<div style={{flex: 1, height: 84, borderRadius: 14, border: '2px solid #5b5e66', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 32, fontWeight: 700}}>
								Cancel
							</div>
							<div
								style={{
									flex: 1,
									height: 84,
									borderRadius: 14,
									background: pressed ? '#2448d8' : '#335fff',
									display: 'flex',
									alignItems: 'center',
									justifyContent: 'center',
									fontSize: 32,
									fontWeight: 800,
									transform: `scale(${pressed ? 0.97 : 1})`,
								}}
							>
								Buy
							</div>
						</div>
					</>
				) : null}
			</div>
		</AbsoluteFill>
	);
};

export const DisconnectDialog: React.FC<{t: number}> = ({t}) => {
	const o = interpolate(t, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'});
	return (
		<AbsoluteFill style={{background: `rgba(0,0,0,${0.55 * o})`}}>
			<div
				style={{
					position: 'absolute',
					left: 960 - 360,
					top: 540 - 190,
					width: 720,
					height: 380,
					borderRadius: 18,
					background: '#393b3d',
					border: '1px solid #55585c',
					boxShadow: '0 20px 70px rgba(0,0,0,0.7)',
					opacity: o,
					transform: `scale(${0.92 + 0.08 * o})`,
					fontFamily: UI_FONT,
					color: '#fff',
					textAlign: 'center',
				}}
			>
				<div style={{fontSize: 42, fontWeight: 800, marginTop: 34}}>Disconnected</div>
				<div style={{height: 1, background: '#5b5e62', margin: '22px 40px'}} />
				<div style={{fontSize: 30, lineHeight: 1.45, color: '#e3e3e3', padding: '0 50px', fontWeight: 500}}>
					The experience&apos;s server has shut down.
					<br />
					(Error Code: 288)
				</div>
				<div style={{position: 'absolute', left: 50, right: 50, bottom: 36, display: 'flex', gap: 22}}>
					<div style={{flex: 1, height: 76, borderRadius: 12, background: '#fff', color: '#222', fontSize: 32, fontWeight: 800, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
						Leave
					</div>
					<div style={{flex: 1, height: 76, borderRadius: 12, border: '2px solid #8a8d92', fontSize: 32, fontWeight: 700, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
						Reconnect
					</div>
				</div>
			</div>
		</AbsoluteFill>
	);
};

export const AlertBanner: React.FC<{t: number; from: number; text: string}> = ({t, from, text}) => {
	if (t < from) return null;
	const k = t - from;
	const flash = 0.75 + 0.25 * Math.sin(k * 12);
	const slide = Math.min(1, k / 0.25);
	return (
		<div style={{position: 'absolute', left: 640, right: 340, top: 26, display: 'flex', justifyContent: 'center', transform: `translateY(${(1 - slide) * -60}px)`, opacity: slide}}>
			<div
				style={{
					padding: '14px 40px',
					borderRadius: 16,
					background: `rgba(200,0,0,${0.85 * flash})`,
					border: '4px solid #1a0000',
					fontFamily: '"Fredoka", "Noto Color Emoji", sans-serif',
					fontWeight: 700,
					fontSize: 36,
					color: '#fff',
					WebkitTextStroke: '6px #1a0000',
					whiteSpace: 'nowrap',
					paintOrder: 'stroke fill',
					boxShadow: '0 0 40px rgba(255,0,0,0.6)',
				}}
			>
				{text}
			</div>
		</div>
	);
};
