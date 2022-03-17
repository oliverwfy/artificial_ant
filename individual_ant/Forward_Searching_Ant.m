% Forward-Searching Ant
%% Set up
%Select Parameters
tmax=500; %stop the ant after tmax time steps.

% Create Grid (nb the grid is toroidal)
% Santa Fe trail:
G=zeros(32);
G(1,2:4)=1;G(1:6,4)=1;G(6,4:7)=1;G(6,9:13)=1;
G(6:10,13)=1;G(12:15,13)=1;G(18:24,13)=1;G(25,8:12)=1;G(25,4:5)=1;
G(26:29,2)=1;G(31,3:6)=1;G(29:30,8)=1;G(28,9:15)=1;G(25:27,17)=1;
G(19:22,17)=1;G(16,18)=1;G(14:15,21)=1;G(8:11,21)=1;G(6,22:23)=1;
G(4:5,25)=1;G(3,26:28)=1;G(4:5,30)=1;G(7,30)=1;G(10,30)=1;G(13,30)=1;
G(15,27:29)=1;G(16,24)=1;G(19,25)=1;G(20,28)=1;G(23,27)=1;G(24,24)=1;

G_Initial=G; %create a copy of G that won't change
n=length(G_Initial); 
scoreMax=sum(G_Initial(:));

% Initialise counters/ trackers
score=0; %score increases by 1 for each piece of food eaten.
A=[1,1;0,1]; %initialise the state of the ant. The first row refers
% to the (row and column) position of the ant. Nb [0,0] is actually
% [32,32] (modular arithmetic).
% The second row gives the direction of the ant: N:[-1,0], E:[0,1], 
% S:[1,0], W:[0,-1].
time=0;
j=0; %this is the counter to keep track of where we are in the algorithm that we apply when there's no food ahead.
G_long=zeros(32,32,tmax+1); %3d matrix keeping a record of the state of G at each time step
G_long(:,:,1)=G_Initial; %NB the state at time t is recorded in the t+1th position (in the third dimension)
A_long=zeros(2,2,tmax+1); %same but for A
A_long(:,:,1)=A; 

%% RELEASE THE ANT!
for t=1:tmax
    time=time+1;
    if ahead(G,A,n)==1 %if food ahead then move forward and eat it
        [G,A,score]=move_eat(G,A,score,n);
        j=0; %reset the counter when the ant eats food
    else 
        j=j+1;
        if mod(j,5)==0
            A(1,:)=mod(A(1,:)+A(2,:),n); %move forward
        else 
            A(2,:)=([0,-1;1,0]*A(2,:)')'; %turn left
        end
    
    end


    % Update the Longs
    G_long(:,:,t+1)=G; 
    A_long(:,:,t+1)=A;
    
    % Check if all the food has been found
    if score==scoreMax
        break
    end
end
result=[score,time]

%% Local Functions
function foodAhead=ahead(G,A,n)

% A function to find whether or not there is food directly in front of the
% ant. 
% INPUT: G, the current grid state
%        A, the ant state
% OUTPUT: {0,1} depending on whether or not there is food directly in front
% of the ant.

 fP=mod(A(1,:)+A(2,:),n); %the position of the tile in front of the ant
 fP=mod(fP-1,n)+1; %guarantee the forward position is in a form that makes sense (i.e. no zero values)
    
 foodAhead=G(fP(1),fP(2));
end

function [G,A,score]=move_eat(G,A,score,n)
% A function to move the ant forward, remove the food on the tile, and add
% one to the score
 A(1,:)=mod(A(1,:)+A(2,:),n); %moves the ant forward one place.
 A(1,:)=mod(A(1,:)-1,n)+1; %converts to 32-form
 
 score=score+1; %update the score
 G(A(1,1),A(1,2))=0; %remove the food
 
 A(1,:)=mod(A(1,:),n); %change back to zero-form


end

