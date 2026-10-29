import React, {useEffect, useState} from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame, useDelayRender} from 'remotion';
import '@fontsource/source-sans-3/400.css';
import '@fontsource/source-sans-3/600.css';
import '@fontsource/source-sans-3/700.css';
import '@fontsource/source-sans-3/800.css';
import '@fontsource/fredoka/600.css';
import '@fontsource/fredoka/700.css';
import '@fontsource/bebas-neue/400.css';
import {f, FPS, MUSIC_CUES, SCENES, SFX_CUES, VOICE_CUES, voiceFile} from './timeline';
import {ColdOpen3, EndCard3, InsideScene, OutsideScene} from './scenes/ReqPart3';
import {Captions, Touches} from './ui/HUD';

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

const Sound: React.FC = () => (
	<>
		{MUSIC_CUES.map((m, i) => {
			const len = f(m.to) - f(m.from);
			const fi = f(m.fadeIn ?? 0.05);
			const fo = f(m.fadeOut ?? 0.3);
			return (
				<Sequence key={'m' + i} from={f(m.from)} durationInFrames={len}>
					<Audio src={staticFile(`music/${m.id}.wav`)} startFrom={f(m.offset ?? 0)} volume={(fr) => m.vol * Math.min(1, fi ? fr / fi : 1, fo ? (len - fr) / fo : 1)} />
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
				<ColdOpen3 />
			</Sequence>
			<Sequence {...span(...SCENES.night)}>
				<OutsideScene t0={SCENES.night[0]} mode="night" />
			</Sequence>
			<Sequence {...span(...SCENES.inside)}>
				<InsideScene t0={SCENES.inside[0]} mode="inside" />
			</Sequence>
			<Sequence {...span(...SCENES.run)}>
				<InsideScene t0={SCENES.run[0]} mode="run" />
			</Sequence>
			<Sequence {...span(...SCENES.outside)}>
				<OutsideScene t0={SCENES.outside[0]} mode="outside" />
			</Sequence>
			<Sequence {...span(...SCENES.out)}>
				<OutsideScene t0={SCENES.out[0]} mode="out" />
			</Sequence>
			<Sequence {...span(...SCENES.end)}>
				<EndCard3 t0={SCENES.end[0]} />
			</Sequence>
			<Overlays />
			<Sound />
		</AbsoluteFill>
	);
};
