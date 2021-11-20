%% LTI System Model

K=5; %approximately
% Function is theta_new = theta + K*(PWM_Diff_Between_Motors)
A=1;
B=K;
C=1;
D=0;
% state-space model into MATLAB
cruise=ss(A,B,C,D);

%% transfer function
% state space model to transfer function conversion
[q,p]=ss2tf(A,B,C,D);
% returns num denum
Gp=tf(q,p);

H=[1];

Kp=2;
Ki=1.5;
Kd=0.8;
Gc=pid(Kp,Ki,Kd);
Mc=feedback(Gc*Gp,H);
step(Mc);
hold on;
