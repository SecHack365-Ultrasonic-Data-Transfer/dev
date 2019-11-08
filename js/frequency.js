const getFreqObject = (freq, type) => {
  const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  const oscillator = audioCtx.createOscillator();
  
  oscillator.frequency.setValueAtTime(freq, audioCtx.currentTime);
  oscillator.connect(audioCtx.destination);
  oscillator.type = type || 'square';
  return oscillator;
}

// 14000Hz
const Hz = 14000;
const fq = getFreqObject(Hz);
// play
fq.start();
// stop
fq.stop();
