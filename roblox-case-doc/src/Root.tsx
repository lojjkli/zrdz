import {Composition} from 'remotion';
import {Doc, TOTAL} from './Doc';

export const Root = () => (
  <Composition id="Doc" component={Doc} durationInFrames={TOTAL} fps={30} width={1920} height={1080} />
);
