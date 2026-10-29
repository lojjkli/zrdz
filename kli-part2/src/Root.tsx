import {Composition} from 'remotion';
import {Video} from './Video';
import {FPS, H, TOTAL, W} from './timeline';

export const RemotionRoot = () => (
	<Composition id="KLI" component={Video} durationInFrames={TOTAL} fps={FPS} width={W} height={H} />
);
