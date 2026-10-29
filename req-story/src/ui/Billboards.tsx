import React from 'react';
import {Cam, project, V3} from '../three/cam';
import {ChatBubble, Nametag, VoiceBubble} from './HUD';

export type BB = {p: V3; name?: string; talking?: boolean; bubble?: {text: string; age: number} | null; hearts?: number};

// Nametags, voice-chat indicators and bubble chat that follow 3D characters.
export const Billboards: React.FC<{cam: Cam; items: BB[]; t: number}> = ({cam, items, t}) => (
	<>
		{items.map((it, i) => {
			const s = project(cam, [it.p[0], it.p[1] + 5.7, it.p[2]]);
			if (!s || s.x < -200 || s.x > 2120 || s.y < -200 || s.y > 1280) return null;
			const scale = Math.max(0.62, Math.min(1.25, 18 / s.dist));
			const y = it.name ? s.y - 40 * scale : s.y;
			return (
				<React.Fragment key={i}>
					{it.name ? <Nametag x={s.x} y={s.y} name={it.name} scale={scale} /> : null}
					{it.talking ? <VoiceBubble x={s.x} y={y - 6 * scale} t={t} scale={scale} /> : null}
					{it.bubble && !it.talking ? <ChatBubble x={s.x} y={y - 6 * scale} text={it.bubble.text} age={it.bubble.age} scale={scale} /> : null}
					{it.hearts !== undefined && it.hearts >= 0 && it.hearts < 2.5
						? new Array(6).fill(0).map((_, k) => {
								const a = it.hearts! - k * 0.12;
								if (a < 0) return null;
								const dx = Math.sin(k * 2.1) * 80 * scale + Math.sin(a * 4 + k) * 14;
								return (
									<div
										key={k}
										style={{
											position: 'absolute',
											left: s.x + dx - 24,
											top: s.y - a * 160 * scale - 20,
											fontSize: 48 * scale,
											opacity: Math.max(0, 1 - a / 2.2),
											fontFamily: '"Noto Color Emoji"',
										}}
									>
										❤️
									</div>
								);
						  })
						: null}
				</React.Fragment>
			);
		})}
	</>
);
