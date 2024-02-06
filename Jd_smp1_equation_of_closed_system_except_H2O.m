% 化学式中の各成分の係数(式量？)の定義
% Jadeite
n_Jd_Na = 0.973;
n_Jd_Al = 1.00;
n_Jd_Si = 1.99;
n_Jd_H = 0;

% Albite
n_Ab_Na = 1.99;
n_Ab_Al = 1.06;
n_Ab_Si = 2.90;
n_Ab_H = 0;

% Nepheline
n_Ne_Na = 0.98;
n_Ne_Al = 0.98;
n_Ne_Si = 0.99;
n_Ne_H = 0;

% Analcime
n_Anl_Na = 0.99;
n_Anl_Al = 1.10;
n_Anl_Si = 1.93;
n_Anl_H = 2;

% Met1 開放系を扱うときは閉鎖しない成分を抜いてください。
n_Met1_Na = 0;
n_Met1_Al = 0;
n_Met1_Si = 0;

% mass-balance 解はv_Ab, v_Ne, v_Anl, v_Meta_H が出力されます。
A = [n_Ab_Al n_Ne_Al n_Anl_Al 0;
    n_Ab_Si n_Ne_Si n_Anl_Si 0;
    n_Ab_Na n_Ne_Na n_Anl_Na 0
    n_Ab_H n_Ne_H n_Anl_H 1];
B = [-n_Jd_Na;
    -n_Jd_Al;
    -n_Jd_Si;
    0];
X = A \ B; % AX=B

% 解に名前をつけます。
v_Ab = X(1);
v_Ne = X(2); 
v_Anl = X(3); 
v_Meta_H = X(4);

% MetaをMet1に変換
n_Met1_H = v_Meta_H;

% 相互拡散係数の定義(a=LSiSi/LNaNa, b=LSiSI/LAlAl, c=LSiSi/LHH)
syms a b c

% A-coefficientの定義
% A_Ab系
A_AbAb = (n_Ab_Na)^2 * a + (n_Ab_Al)^2 * b + (n_Ab_Si)^2;
A_AbNe = (n_Ab_Na) * (n_Ne_Na) * a + (n_Ab_Al) * (n_Ne_Al) * b + (n_Ab_Si) * (n_Ne_Si);
A_AbJd = (n_Ab_Na) * (n_Jd_Na) * a + (n_Ab_Al) * (n_Jd_Al) * b + (n_Ab_Si) * (n_Jd_Si);
A_AbMet1 = (n_Ab_Na) * (n_Met1_Na) * a + (n_Ab_Al) * (n_Met1_Al) * b + (n_Ab_Si) * (n_Met1_Si) + (n_Ab_H) * (n_Met1_H) * c;
A_AbAnl = (n_Ab_Na) * (n_Anl_Na) * a + (n_Ab_Al) * (n_Anl_Al) * b + (n_Ab_Si) * (n_Anl_Si) + (n_Ab_H) * (n_Anl_H) * c;

% A_Ne系
A_NeAb = (n_Ab_Na) * (n_Ne_Na) * a + (n_Ab_Al) * (n_Ne_Al) * b + (n_Ab_Si) * (n_Ne_Si);
A_NeNe = (n_Ne_Na)^2 * a + (n_Ne_Al)^2 * b + (n_Ne_Si)^2;
A_NeJd = (n_Ne_Na) * (n_Jd_Na) * a + (n_Ne_Al) * (n_Jd_Al) * b + (n_Ne_Si) * (n_Jd_Si);
A_NeMet1 = (n_Ne_Na) * (n_Met1_Na) * a + (n_Ne_Al) * (n_Met1_Al) * b + (n_Ne_Si) * (n_Met1_Si) + (n_Ne_H) * (n_Met1_H) * c;
A_NeAnl = (n_Ne_Na) * (n_Anl_Na) * a + (n_Ne_Al) * (n_Anl_Al) * b + (n_Ne_Si) * (n_Anl_Si) + (n_Ne_H) * (n_Anl_H) * c;

% A_Anl系
A_AnlAb = (n_Anl_Na) * (n_Ab_Na) * a + (n_Anl_Al) * (n_Ab_Al) * b + (n_Anl_Si) * (n_Ab_Si);
A_AnlNe = (n_Anl_Na) * (n_Ne_Na) * a + (n_Anl_Al) * (n_Ne_Al) * b + (n_Anl_Si) * (n_Ne_Si);
A_AnlAnl = (n_Anl_Na)^2 * a + (n_Anl_Al)^2 * b + (n_Anl_Si)^2 + (n_Anl_H)^2 * c;
A_AnlJd = (n_Anl_Na) * (n_Jd_Na) * a + (n_Anl_Al) * (n_Jd_Al) * b + (n_Anl_Si) * (n_Jd_Si);
A_AnlMet1 = (n_Anl_Na) * (n_Met1_Na) * a + (n_Anl_Al) * (n_Met1_Al) * b + (n_Anl_Si) * (n_Met1_Si) + (n_Anl_H) * (n_Met1_H) * c;

% 連立方程式(解はv_1_Ab, v_1_Ne, v_2_Ab, v_2_Ne, v_2_Anl, v_3_Ab, v_3_Anl, v_4_Anl)
C = [A_AbAb A_AbNe 0 0 0 0 0 0;
    A_NeAb A_NeNe 0 0 0 0 0 0;
    A_AbAb 0 A_AbAb 0 A_AbAnl 0 0 0;
    A_AnlAb 0 A_AnlAb 0 A_AnlAnl 0 0 0;
    0 1 0 1 0 0 0 0;
    0 0 0 0 A_AnlAnl 0 A_AnlAnl 0;
    1 0 1 0 0 1 0 0;
    0 0 0 0 1 0 1 1 ];
D = [-A_AbMet1-A_AbJd;
    -A_NeMet1-A_NeJd;
    -A_AbMet1-A_AbJd-A_AbNe*v_Ne; 
    -A_AnlMet1-A_AnlJd-A_AnlNe*v_Ne; 
    v_Ne;
    -A_AnlMet1-A_AnlJd-A_AnlNe*v_Ne-A_AnlAb*v_Ab;
    v_Ab;
    v_Anl];
Y = C \ D; % CY=D

% 解の表示
disp('v_Ab, v_Ne, v_Anl, v_Meta_H:');
disp(X);

disp('v_1_Ab, v_1_Ne, v_2_Ab, v_2_Ne, v_2_Anl, v_3_Ab, v_3_Anl, v_4_Anl:');
disp(Y);