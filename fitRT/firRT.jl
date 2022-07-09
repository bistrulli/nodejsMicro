using Printf,Ipopt,Plots,JuMP,MAT,ProgressBars,ParameterJuMP,Statistics,CPLEX

DATA = matread("/Users/emilio/git/nodejsMicro/data/3tier_tofit.mat")

#genero la matrice dei jump in modo automatico a seconda della dimensione
function genStoich(n)
        stoich_matrix=zeros(n*(n-1),n)
        k=0;
        for i=1:n
                for j=1:n
                        if(j!=i)
                                #qui so che sto andando dalla sazioni i alla stazione j
                                k=k+1;
                                stoich_matrix[k,i]=-1;
                                stoich_matrix[k,j]=1;
                        end
                end
        end
        return stoich_matrix
end

nzIdz=sum(DATA["RTm"],dims=2).!=0

Cli=zeros(sum(nzIdz),1)
Tm=zeros(sum(nzIdz),size(DATA["Tm"],2))
RTm=zeros(sum(nzIdz),size(DATA["RTm"],2))
NC=zeros(sum(nzIdz),size(DATA["NC"],2))

for i=1:sum(nzIdz)
        if(DATA["Cli"][i]!=0)
                global Cli[i]=DATA["Cli"][i]
                global Tm[i,:]=DATA["Tm"][i,:]
                global RTm[i,:]=DATA["RTm"][i,:]/1000.
                global NC[i,:]=DATA["NC"][i,:]
        end
end


#model = Model(()->MadNLP.Optimizer(linear_solver=MadNLPLapackCPU,max_iter=100000))
#model = Model(Ipopt.Optimizer)
model = Model(CPLEX.Optimizer)
#set_optimizer_attribute(model, "linear_solver", "pardiso")
#set_optimizer_attribute(model, "max_iter", 20000)
# set_optimizer_attribute(model, "derivative_test", "first-order")
# set_optimizer_attribute(model, "check_derivatives_for_naninf", "yes")

npoints=size(RTm,1)
N=size(RTm,2)

B=10^4

@variable(model,RTlqn[i=1:N,p=1:npoints]>=0)
@variable(model,RTs[i=1:N]>=0)
@variable(model,X[i=1:N,j=1:N],Bin)
@variable(model,P[i=1:N,j=1:N]>=0)
@variable(model,E_abs[i=1:N,j=1:npoints]>=0)
@constraint(model,sum(P,dims=2).<=(N-1))
@constraint(model,P.<=1)
@constraint(model,[i=1:N],P[i,i]==0)

for i=1:N
        for j=1:N
                @constraint(model,P[i,j]<=(X[i,j]))
                @constraint(model,-P[i,j]<=-10^(-4)+(1-X[i,j]))
        end
end


for p=1:npoints
        #per ogni stazione
        for i=1:N
                #constraints per definire la norma L1 sul tempo di risposta
                #lego le grandezze con la nuova relazione
                #@NLconstraint(model,RTlqn[i,p]==sum(P[i,j]*RTlqn[j,p] for j=1:N)+RTs[i])
                @constraint(model,RTlqn[i,p]==sum(P[i,j]*RTm[p,j] for j=1:N)+RTs[i])
                @constraint(model,E_abs[i,p]>=(RTlqn[i,p]-RTm[p,i]))
                @constraint(model,E_abs[i,p]>=(-RTlqn[i,p]+RTm[p,i]))
        end

end

# @constraint(model,X[1,2]+X[2,1]+X[1,3]+X[3,1]+X[2,3]+X[3,2]<=1)
@constraint(model,X[1,2]+X[2,1]<=1)
#@constraint(model,X[2,3]+X[3,2]<=1)
@constraint(model,X[3,1]+X[3,2]==0)

#@objective(model,Min, sum(E_abs2[i,p] for i=1:size(E_abs2,1) for p=1:size(E_abs2,2))+sum(E_abs[i,p] for i=1:size(E_abs,1) for p=1:size(E_abs,2))+sum(ERT_abs[i,p] for i=1:size(ERT_abs,1) for p=1:size(E_abs,2)))
@objective(model,Min,sum(E_abs[i,p] for i=1:size(E_abs,1) for p=1:size(E_abs,2)))
#@objective(model,Min, sum(E_abs2))
JuMP.optimize!(model)

# matwrite("fromJulia.mat", Dict(
# "RTlqn" => value.(RTlqn),
# "T" => value.(T),
# "MU" => value.(MU),
# "P" => value.(P),
# "P2" => value.(P.*P2),
# "NCopt" => value.(NC)
# );)
