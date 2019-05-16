close all; clc;clear;
 
path.data = 'C:\Users\Jesper W Henriksen\Documents\Med10\Code\Matlab\Logs\';
%Participant path
path.p = 'P1\';
path.lego = 'Lego\';                  
path.water = 'Water\';
data.fr = 30;                            
data.Fs = data.fr;
%change this to either RGB, thermal or depth
path.finalpath = [path.data path.water];
%change p Path to change participant
path.finalpath = [path.finalpath path.p];       


files=dir(path.finalpath);
A = readmatrix([path.finalpath files(3).name()]);
ecgdata = load([path.finalpath files(3).name()]);


%% Plotting section
figure(1);
plot(signal);
ylabel('Green Value');
xlabel('Image Index');

msig = signal - movmean(signal, 40);
figure(2);
plot(msig);
ylabel('Magnitude');
xlabel('Image Index');
 
[b,a] = butter(4,[0.7 4]/(data.fr/2));
fsignal = filterSignals(msig',b,a);
figure(3);
plot(fsignal);
ylabel('Magnitude');
xlabel('Image Index');
isignal = interpolateSignals(fsignal,data.fr,250);
figure(4);
plot(isignal);
ylabel('Magnitude');
xlabel('Index');
 
%s = modes(5,:);
s = isignal;
[~,ps,f] = computeFourierTransforms(s,250);%data.Fs);
 
figure(5);
subplot(2,1,1); hold on;
plot((1:length(s))/data.fr, s ,'k');
xlabel('time(s)');
ylabel('');
title('Signal');
subplot(2,1,2);
plot(f,ps,'k');
xlim([0 8])
xlabel('Frequency (Hz)');
ylabel('Power');
[value,index] = max(ps);
freq = 0:250/length(s):250/2;
max_power = freq(index)
pulseColor = max_power * 60
 
 
%ECG TRUE VALUE = 75
data.sensitivity = 2.5;
qsr.qsrraw = load([path.ecgdata 'ECG.mat']);
qsr.qsr = qsr.qsrraw.ecg;
pulseQSR = getQSR2(qsr.qsr,60,255,data.sensitivity);