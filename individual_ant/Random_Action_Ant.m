% Random Action Ant

% !Need to check it for errors. Perhaps alter it so you can see the ant
% move.
%% Set up
%Select Parameters
tmax=500; %stop the ant after tmax time steps.
n=32; %size of the square grid.
% Create Grid and trail (nb the grid is toroidal)
% Santa Fe trail:
G=zeros(32);
G(1,2:4)=1;G(1:6,4)=1;G(6,4:7)=1;G(6,9:13)=1;
G(6:10,13)=1;G(12:15,13)=1;G(18:24,13)=1;G(25,8:12)=1;G(25,4:5)=1;
G(26:29,2)=1;G(31,3:6)=1;G(29:30,8)=1;G(28,9:15)=1;G(25:27,17)=1;
G(19:22,17)=1;G(16,18)=1;G(14:15,21)=1;G(8:11,21)=1;G(6,22:23)=1;
G(4:5,25)=1;G(3,26:28)=1;G(4:5,30)=1;G(7,30)=1;G(10,30)=1;G(13,30)=1;
G(15,27:29)=1;G(16,24)=1;G(19,25)=1;G(20,28)=1;G(23,27)=1;G(24,24)=1;

G_Initial=G; %create a copy of G that won't change
n=length(G_Initial); %length/width of G
% Initialise counters/ trackers
score=0; %score increases by 1 for each piece of food eaten.
A=[1,1;0,1]; %initialise the state of the ant. The first row refers
% to the (row and column) position of the ant. Nb [0,0] is actually
% [32,32] (modular arithmetic).
% The second row gives the direction of the ant: N:[-1,0], E:[0,1], 
% S:[1,0], W:[0,-1].
time=0;

G_long=zeros(32,32,tmax+1); %3d matrix keeping a record of the state of G at each time step
G_long(:,:,1)=G_Initial; %NB the state at time t is recorded in the t+1th position (in the third dimension)
A_long=zeros(2,2,tmax+1); %same but for A
A_long(:,:,1)=A; 

%% RELEASE THE ANT!
for t=1:tmax
    time=time+1;
    % Move/rotate the ant.
    r3=randi(3); %(uniformly) random member of {1,2,3}
    if r3==1 %then move the ant forward one place:
        A(1,:)=mod(A(1,:)+A(2,:),n);
    elseif r3==2 %then rotate ant left:
        A(2,:)=([0,-1;1,0]*A(2,:)')';
    else %rotate ant right:
        A(2,:)=([0,1;-1,0]*A(2,:)')';
    end
    % Does the ant eat?
    A(1,:)=mod(A(1,:)-1,n)+1; %if either position value is 0, this changes 
    % it to n (can't look at the 0th row/col of G)
    if G(A(1,1),A(1,2))==1 %check if the ant is on a tile w/ food
        score=score+1; %update the score
        G(A(1,1),A(1,2))=0; %remove the food
    end
    A(1,:)=mod(A(1,:),n); %change back to zero-position form
    if score==sum(G_Initial(:))
        break
    end

    G_long(:,:,t+1)=G; 
    A_long(:,:,t+1)=A;
end
result=[score,time]






