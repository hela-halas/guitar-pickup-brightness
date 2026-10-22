% Original MATLAB (R2023a) analysis script from the 2023 Extended Essay,
% transcribed from the essay appendix and kept unchanged for reference.
% The maintained version is src/pickup_brightness.py.

% MagnitudeMlast.m opens five files E2-SMn-1.wav to E2-SMn-5.wav
% calculates DFT of sound for each of the files using MATLAB's fft function
% calculates magnitudes of harmonics (1-9)
% E2-SMn-1.m to E2-SMn-5.m contain recordings of string E2 with pickup located at MPP
Fs = 44100;   % sampling freq [Hz]
Ts = 1/Fs;   % sampling period
start = 1;
finish = 398426;   % end of shortest recording
% reading audio sample no. 1
ystereo = audioread('E2-SMn-1.wav');
[a,b] = size(ystereo);
% if sound is in stereo, changes stereo to mono
if b>1,
ymono = (ystereo(:,1)+ystereo(:,2))/2;
y = ymono';
else
y = ystereo;
end
% calculation of DFT
stable_y = y(start:finish);
stable_y_N = length(stable_y);   % number of samples
DFTstabley = fft(stable_y,stable_y_N);   % DFT of audio
absDFT(1,:) = abs(DFTstabley);   % Magnitude of the DFT
freq_step = Fs/stable_y_N;   % freq step on DFT scale
freqscale = (0:(stable_y_N-1))*Fs/stable_y_N;   % x axis for plotting, frequency
% searches for the specific frequency at which the magnitude spike occurs M(1,:)
% searches for the magnitude of the spike M(2,:)
miles = round(83/freq_step)-20; davis = round(83/freq_step)+20;
[m,i]=max(absDFT(1, 1:davis)); M1(1,1)=i; M1(2,1)=m;
miles = round(163/freq_step)-20; davis = round(163/freq_step)+20;
[m,i]=max(absDFT(1, miles:davis)); M1(1,2)=i+miles-1; M1(2,2)=m;
miles = round(245/freq_step)-20; davis = round(245/freq_step)+20;
[m,i]=max(absDFT(1, miles:davis)); M1(1,3)=i+miles-1; M1(2,3)=m;
miles = round(328/freq_step)-20; davis = round(328/freq_step)+20;
[m,i]=max(absDFT(1, miles:davis)); M1(1,4)=i+miles-1; M1(2,4)=m;
miles = round(410/freq_step)-20; davis = round(410/freq_step)+20;
[m,i]=max(absDFT(1, miles:davis)); M1(1,5)=i+miles-1; M1(2,5)=m;
miles = round(493/freq_step)-20; davis = round(493/freq_step)+20;
[m,i]=max(absDFT(1, miles:davis)); M1(1,6)=i+miles-1; M1(2,6)=m;
miles = round(575/freq_step)-20; davis = round(575/freq_step)+20;
[m,i]=max(absDFT(1, miles:davis)); M1(1,7)=i+miles-1;M1(2,7)=m;
miles = round(658/freq_step)-20; davis = round(658/freq_step)+20;
[m,i]=max(absDFT(1, miles:davis)); M1(1,8)=i+miles-1; M1(2,8)=m;
miles = round(741/freq_step)-20; davis = round(741/freq_step)+20;
[m,i]=max(absDFT(1, miles:davis)); M1(1,9)=i+miles-1; M1(2,9)=m;
% reading audio sample no. 2
ystereo = audioread('E2-SMn-2.wav');
[a,b] = size(ystereo);
if b>1,
ymono = (ystereo(:,1)+ystereo(:,2))/2;   % y - stereo sound change to mono
y = ymono';
else
y = ystereo;
end
% calculation of DFT
stable_y = y(start:finish);
stable_y_N = length(stable_y);   % N - number of samples
DFTstabley = fft(stable_y,stable_y_N);   % DFT of audio
absDFT(2,:) = abs(DFTstabley);   % Magnitude of the DFT
freq_step = Fs/stable_y_N;   % freq step on DFT scale
freqscale = (0:(stable_y_N-1))*Fs/stable_y_N;   % x axis for plot, frequency
% searches for the specific frequency at which the magnitude spike occurs M(1,:)
% searches for the magnitude of the spike M(2,:)
miles = round(83/freq_step)-20; davis = round(83/freq_step)+20;
[m,i]=max(absDFT(2, 1:davis)); M2(1,1)=i; M2(2,1)=m;
miles = round(163/freq_step)-20; davis = round(163/freq_step)+20;
[m,i]=max(absDFT(2, miles:davis)); M2(1,2)=i+miles-1; M2(2,2)=m;
miles = round(245/freq_step)-20; davis = round(245/freq_step)+20;
[m,i]=max(absDFT(2, miles:davis)); M2(1,3)=i+miles-1; M2(2,3)=m;
miles = round(328/freq_step)-20; davis = round(328/freq_step)+20;
[m,i]=max(absDFT(2, miles:davis)); M2(1,4)=i+miles-1; M2(2,4)=m;
miles = round(410/freq_step)-20; davis = round(410/freq_step)+20;
[m,i]=max(absDFT(2, miles:davis)); M2(1,5)=i+miles-1; M2(2,5)=m;
miles = round(493/freq_step)-20; davis = round(493/freq_step)+20;
[m,i]=max(absDFT(2, miles:davis)); M2(1,6)=i+miles-1; M2(2,6)=m;
miles = round(575/freq_step)-20; davis = round(575/freq_step)+20;
[m,i]=max(absDFT(2, miles:davis)); M2(1,7)=i+miles-1; M2(2,7)=m;
miles = round(658/freq_step)-20; davis = round(658/freq_step)+20;
[m,i]=max(absDFT(2, miles:davis)); M2(1,8)=i+miles-1; M2(2,8)=m;
miles = round(741/freq_step)-20; davis = round(741/freq_step)+20;
[m,i]=max(absDFT(2, miles:davis)); M2(1,9)=i+miles-1; M2(2,9)=m;
% reading audio sample no. 3
ystereo = audioread('E2-SMn-3.wav');
[a,b] = size(ystereo);
if b>1,
ymono = (ystereo(:,1)+ystereo(:,2))/2;   % y - stereo sound change to mono
y = ymono';
else
y = ystereo;
end
% calculation of DFT
stable_y = y(start:finish);
stable_y_N = length(stable_y);   % N - number of samples
DFTstabley = fft(stable_y,stable_y_N);   % DFT of audio
absDFT(3,:) = abs(DFTstabley);   % Magnitude of the DFT
freq_step = Fs/stable_y_N;   % freq step on DFT scale
freqscale = (0:(stable_y_N-1))*Fs/stable_y_N;   % x axis for plot, frequency
% searches for the specific frequency at which the magnitude spike occurs M(1,:)
% searches for the magnitude of the spike M(2,:)
miles = round(83/freq_step)-20; davis = round(83/freq_step)+20;
[m,i]=max(absDFT(3, 1:davis)); M3(1,1)=i; M3(2,1)=m;
miles = round(163/freq_step)-20; davis = round(163/freq_step)+20;
[m,i]=max(absDFT(3, miles:davis)); M3(1,2)=i+miles-1; M3(2,2)=m;
miles = round(245/freq_step)-20; davis = round(245/freq_step)+20;
[m,i]=max(absDFT(3, miles:davis)); M3(1,3)=i+miles-1; M3(2,3)=m;
miles = round(328/freq_step)-20; davis = round(328/freq_step)+20;
[m,i]=max(absDFT(3, miles:davis)); M3(1,4)=i+miles-1; M3(2,4)=m;
miles = round(410/freq_step)-20; davis = round(410/freq_step)+20;
[m,i]=max(absDFT(3, miles:davis)); M3(1,5)=i+miles-1; M3(2,5)=m;
miles = round(493/freq_step)-20; davis = round(493/freq_step)+20;
[m,i]=max(absDFT(3, miles:davis)); M3(1,6)=i+miles-1; M3(2,6)=m;
miles = round(575/freq_step)-20; davis = round(575/freq_step)+20;
[m,i]=max(absDFT(3, miles:davis)); M3(1,7)=i+miles-1; M3(2,7)=m;
miles = round(658/freq_step)-20; davis = round(658/freq_step)+20;
[m,i]=max(absDFT(3, miles:davis)); M3(1,8)=i+miles-1; M3(2,8)=m;
miles = round(741/freq_step)-20; davis = round(741/freq_step)+20;
[m,i]=max(absDFT(3, miles:davis)); M3(1,9)=i+miles-1; M3(2,9)=m;
% reading audio sample 4
ystereo = audioread('E2-SMn-4.wav');
[a,b] = size(ystereo);
if b>1,
ymono = (ystereo(:,1)+ystereo(:,2))/2;   % y - stereo sound change to mono
y = ymono';
else
y = ystereo;
end
% calculation of FFT
stable_y = y(start:finish);
stable_y_N = length(stable_y);   % N - number of samples
DFTstabley = fft(stable_y,stable_y_N);   % fft of sec audio
absDFT(4,:) = abs(DFTstabley);   % Magnitude of the FFT
freq_step = Fs/stable_y_N;   % freq step on fft scale
freqscale = (0:(stable_y_N-1))*Fs/stable_y_N;   % x axis for plot, frequency
% searches for the specific frequency at which the magnitude spike occurs M(1,:)
% searches for the magnitude of the spike M(2,:)
miles = round(83/freq_step)-20; davis = round(83/freq_step)+20;
[m,i]=max(absDFT(3, 1:davis)); M4(1,1)=i; M4(2,1)=m;
miles = round(163/freq_step)-20; davis = round(163/freq_step)+20;
[m,i]=max(absDFT(4, miles:davis)); M4(1,2)=i+miles-1; M4(2,2)=m;
miles = round(245/freq_step)-20; davis = round(245/freq_step)+20;
[m,i]=max(absDFT(4, miles:davis)); M4(1,3)=i+miles-1; M4(2,3)=m;
miles = round(328/freq_step)-20; davis = round(328/freq_step)+20;
[m,i]=max(absDFT(4, miles:davis)); M4(1,4)=i+miles-1; M4(2,4)=m;
miles = round(410/freq_step)-20; davis = round(410/freq_step)+20;
[m,i]=max(absDFT(4, miles:davis)); M4(1,5)=i+miles-1; M4(2,5)=m;
miles = round(493/freq_step)-20; davis = round(493/freq_step)+20;
[m,i]=max(absDFT(4, miles:davis)); M4(1,6)=i+miles-1; M4(2,6)=m;
miles = round(575/freq_step)-20; davis = round(575/freq_step)+20;
[m,i]=max(absDFT(4, miles:davis)); M4(1,7)=i+miles-1; M4(2,7)=m;
miles = round(658/freq_step)-20; davis = round(658/freq_step)+20;
[m,i]=max(absDFT(4, miles:davis)); M4(1,8)=i+miles-1; M4(2,8)=m;
miles = round(741/freq_step)-20; davis = round(741/freq_step)+20;
[m,i]=max(absDFT(4, miles:davis)); M4(1,9)=i+miles-1; M4(2,9)=m;
% reading audio sample 5
ystereo = audioread('E2-SMn-5.wav');
[a,b] = size(ystereo);
if b>1,
ymono = (ystereo(:,1)+ystereo(:,2))/2;   % y - stereo sound change to mono
y = ymono';
else
y = ystereo;
end
% calculation of FFT
stable_y = y(start:finish);
stable_y_N = length(stable_y);   % N - number of samples
DFTstabley = fft(stable_y,stable_y_N);   % fft of audio
absDFT(5,:) = abs(DFTstabley);   % Magnitude of the FFT
freq_step = Fs/stable_y_N;   % freq step on fft scale
freqscale = (0:(stable_y_N-1))*Fs/stable_y_N;   % x axis for plot, frequenc
% searches for the specific frequency at which the magnitude spike occurs M(1,:)
% searches for the magnitude of the spike M(2,:)
miles = round(83/freq_step)-20; davis = round(83/freq_step)+20;
[m,i]=max(absDFT(5, 1:davis)); M5(1,1)=i; M5(2,1)=m;
miles = round(163/freq_step)-20; davis = round(163/freq_step)+20;
[m,i]=max(absDFT(5, miles:davis)); M5(1,2)=i+miles-1; M5(2,2)=m;
miles = round(245/freq_step)-20; davis = round(245/freq_step)+20;
[m,i]=max(absDFT(5, miles:davis)); M5(1,3)=i+miles-1; M5(2,3)=m;
miles = round(328/freq_step)-20; davis = round(328/freq_step)+20;
[m,i]=max(absDFT(5, miles:davis)); M5(1,4)=i+miles-1; M5(2,4)=m;
miles = round(410/freq_step)-20; davis = round(410/freq_step)+20;
[m,i]=max(absDFT(5, miles:davis)); M5(1,5)=i+miles-1; M5(2,5)=m;
miles = round(493/freq_step)-20; davis = round(493/freq_step)+20;
[m,i]=max(absDFT(5, miles:davis)); M5(1,6)=i+miles-1; M5(2,6)=m;
miles = round(575/freq_step)-20; davis = round(575/freq_step)+20;
[m,i]=max(absDFT(5, miles:davis)); M5(1,7)=i+miles-1; M5(2,7)=m;
miles = round(658/freq_step)-20; davis = round(658/freq_step)+20;
[m,i]=max(absDFT(5, miles:davis)); M5(1,8)=i+miles-1; M5(2,8)=m;
miles = round(741/freq_step)-20; davis = round(741/freq_step)+20;
[m,i]=max(absDFT(5, miles:davis)); M5(1,9)=i+miles-1; M5(2,9)=m;
% harmonics' frequency matrix
H(1,:) = M1(1,:);
H(2,:) = M2(1,:);
H(3,:) = M3(1,:);
H(4,:) = M4(1,:);
H(5,:) = M5(1,:);
H = H * freq_step;
StdH = std(H);
MeanH = mean(H);
% harmonics' magnitudes matrix
M(1,:) = M1(2,:);
M(2,:) = M2(2,:);
M(3,:) = M3(2,:);
M(4,:) = M4(2,:);
M(5,:) = M5(2,:);
StdM = std(M);
MeanM = mean(M);
% Spectral Centroid calculation
Centroid = MeanM * MeanH';
Centroid = Centroid / (MeanM * [1, 1, 1, 1, 1, 1, 1, 1, 1]');
% Brightness Ratio calculation
Br = (MeanM(5:9) * [1, 1, 1, 1, 1]')/ MeanM(1);
% Modified Brightness Ratio
Bra = (MeanM(5:9) * [1, 1, 1, 1, 1]')/ (MeanM(1:4) * [1, 1, 1, 1]');
% plot DFT for 0 - 900Hz
Frange = round(901/freq_step);
plot(freqscale(1:Frange), absDFT(1,1:Frange),'m');hold
plot(freqscale(1:Frange), absDFT(2,1:Frange),'r');
plot(freqscale(1:Frange), absDFT(3,1:Frange),'g');
plot(freqscale(1:Frange), absDFT(4,1:Frange),'c');
plot(freqscale(1:Frange), absDFT(5,1:Frange),'b');
xlabel('1Hz-900Hz signal frequency [Hz]');
ylabel('Magnitude');
title('E2 string stable period, pickup in Bridge position, DFT Magnitude in Frequency Domain');
