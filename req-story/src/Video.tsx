import React, {useEffect, useState} from 'react';
import {AbsoluteFill, Audio, interpolate, Sequence, staticFile, useCurrentFrame, useDelayRender} from 'remotion';
import '@fontsource/source-sans-3/400.css';
import '@fontsource/source-sans-3/600.css';
import '@fontsource/source-sans-3/700.css';
import '@fontsource/source-sans-3/800.css';
import '@fontsource/fredoka/600.css';
import '@fontsource/fredoka/700.css';
import '@fontsource/bebas-neue/400.css';
import {f, FPS, MUSIC_CUES, SCENES, SFX_CUES, VOICE_CUES, voiceFile} from './timeline';
import {AppScene, ColdOpen, EndCard} from './scenes/Doc';
import {SpawnScene} from './scenes/Spawn';
import {MachineScene, SadScene} from './scenes/Machine';
import {ArrivalScene, WeddingScene} from './scenes/Love';
import {ChaseScene, IMPACT} from './scenes/Chase';
import {Captions, Touches} from './ui/HUD';
import {DisconnectDialog} from './ui/Dialogs';

const span = (a: number, b: number) => ({from: f(a), durationInFrames: f(b) - f(a)});

const Overlays: React.FC = () => {
	const t = useCurrentFrame() / FPS;
	return (
		<>
			<Touches t={t} />
			<Captions t={t} />
		</>
	);
};

const Disconnect: React.FC<{t0: number}> = ({t0}) => {
	const t = t0 + useCurrentFrame() / FPS;
	return (
		<AbsoluteFill style={{background: '#000'}}>
			<AbsoluteFill style={{filter: 'blur(5px) brightness(0.55) saturate(0.7)'}}>
				<ChaseScene t0={82} freezeAt={IMPACT - 0.25} />
			</AbsoluteFill>
			<DisconnectDialog t={t - t0 - 0.4} />
			<AbsoluteFill style={{background: '#fff', opacity: interpolate(t - t0, [0, 0.35], [1, 0], {extrapolateRight: 'clamp'})}} />
			<AbsoluteFill style={{background: '#000', opacity: interpolate(t, [92.4, 93], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}} />
		</AbsoluteFill>
	);
};

const Sound: React.FC = () => (
	<>
		{MUSIC_CUES.map((m, i) => {
			const len = f(m.to) - f(m.from);
			const fi = f(m.fadeIn ?? 0.05);
			const fo = f(m.fadeOut ?? 0.3);
			return (
				<Sequence key={'m' + i} from={f(m.from)} durationInFrames={len}>
					<Audio
						src={staticFile(`music/${m.id}.wav`)}
						startFrom={f(m.offset ?? 0)}
						volume={(fr) =>
							m.vol * Math.min(1, fi ? fr / fi : 1, fo ? (len - fr) / fo : 1)
						}
					/>
				</Sequence>
			);
		})}
		{VOICE_CUES.map((v, i) => (
			<Sequence key={'v' + i} from={f(v.at)}>
				<Audio src={staticFile(voiceFile(v.id))} volume={v.vol ?? 1} />
			</Sequence>
		))}
		{SFX_CUES.map((s, i) => (
			<Sequence key={'s' + i} from={f(s.at)} durationInFrames={s.dur ? f(s.dur) : undefined}>
				<Audio src={staticFile(`sfx/${s.id}.wav`)} volume={s.vol ?? 1} />
			</Sequence>
		))}
	</>
);

const useFonts = () => {
	const [ready, setReady] = useState(false);
	const {delayRender, continueRender} = useDelayRender();
	const [handle] = useState(() => delayRender('fonts'));
	useEffect(() => {
		Promise.all(
			['400 30px "Source Sans 3"', '600 30px "Source Sans 3"', '700 30px "Source Sans 3"', '800 30px "Source Sans 3"', '700 30px "Fredoka"', '600 30px "Fredoka"', '400 30px "Bebas Neue"', '30px "Noto Color Emoji"'].map((ff) =>
				document.fonts.load(ff, 'A💎'),
			),
		)
			.catch(() => undefined)
			.then(() => {
				setReady(true);
				continueRender(handle);
			});
	}, [continueRender, handle]);
	return ready;
};

export const Video: React.FC = () => {
	const ready = useFonts();
	if (!ready) return <AbsoluteFill style={{background: '#000'}} />;
	return (
		<AbsoluteFill style={{background: '#000'}}>
			<Sequence {...span(...SCENES.cold)}>
				<ColdOpen />
			</Sequence>
			<Sequence {...span(...SCENES.app)}>
				<AppScene t0={SCENES.app[0]} />
			</Sequence>
			<Sequence {...span(...SCENES.spawn)}>
				<SpawnScene t0={SCENES.spawn[0]} />
			</Sequence>
			<Sequence {...span(...SCENES.machine)}>
				<MachineScene t0={SCENES.machine[0]} />
			</Sequence>
			<Sequence {...span(...SCENES.sad)}>
				<SadScene t0={SCENES.sad[0]} />
			</Sequence>
			<Sequence {...span(...SCENES.arrival)}>
				<ArrivalScene t0={SCENES.arrival[0]} />
			</Sequence>
			<Sequence {...span(SCENES.wedding[0], 82)}>
				<WeddingScene t0={SCENES.wedding[0]} />
			</Sequence>
			<Sequence {...span(82, SCENES.collapse[1])}>
				<ChaseScene t0={82} />
			</Sequence>
			<Sequence {...span(...SCENES.disconnect)}>
				<Disconnect t0={SCENES.disconnect[0]} />
			</Sequence>
			<Sequence {...span(...SCENES.end)}>
				<EndCard t0={SCENES.end[0]} />
			</Sequence>
			<Overlays />
			<Sound />
		</AbsoluteFill>
	);
};
