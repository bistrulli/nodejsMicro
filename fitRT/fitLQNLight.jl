using NLopt,AmplNLWriter,Couenne_jll,Printf,Ipopt,MadNLP,Plots,MadNLPMumps,JuMP,MAT,ProgressBars,ParameterJuMP,Statistics,CPLEX

#riscrivo il problema non cercandolo di risolverlo per mu
#a partre dai throughput misurati cerco di capire tutte le P
#imposto le P2 (posso farlo sia lineare che non, )
#calolo i MU grazie alle P2 e i tempi di riposta misurati a singolo client (altrimenti li risolvo con un problema di ottimizzazione sucessivo)

#devo modificare lo script in modo da fare predizione a partire da altri parametri

DATA = matread("/Users/emilio/git/nodejsMicro/data/3tier1b.mat")

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
RTm=zeros(sum(nzIdz),size(DATA["RTm"],2))/1000
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
model = Model(Ipopt.Optimizer)
#model = Model(CPLEX.Optimizer)
#set_optimizer_attribute(model, "linear_solver", "pardiso")
#set_optimizer_attribute(model, "max_iter", 20000)
# set_optimizer_attribute(model, "derivative_test", "first-order")
# set_optimizer_attribute(model, "check_derivatives_for_naninf", "yes")

# set_optimizer_attribute(model, "tol", 10^-15)
# set_optimizer_attribute(model, "acceptable_tol", 10^-15)
#set_optimizer_attribute(model, "hessian_approximation", "limited-memory")
#set_optimizer_attribute(model, "print_level", 0)

jump=genStoich(size(Tm,2))
npoints=size(RTm,1)

mmu=1 ./minimum(RTm,dims=1)

@variable(model,T[i=1:size(jump,1),j=1:npoints]>=0)
@variable(model,RTlqn[i=1:size(jump,2),p=1:npoints]>=0)

@variable(model,X[i=1:size(jump,2),j=1:npoints]>=0)
@variable(model,P[i=1:size(jump,2),j=1:size(jump,2)]>=0)
@variable(model,P2[i=1:size(jump,2),j=1:size(jump,2)]>=0)
@variable(model,RTs[i=1:size(jump,2),j=1:npoints]>=0)
@variable(model,E_abs[p=1:npoints]>=0)
@variable(model,ERT_abs[i=1:size(jump,2),j=1:npoints]>=0)

@constraint(model,sum(P,dims=2).==1)
@constraint(model,P2.<=1)
@constraint(model,P.<=1)
@constraint(model,[i=1:size(P2,1)],P2[i,i]==0)
@constraint(model,[i=1:size(P,1)],P2[i,i]==0)

#@constraint(model,RTs[1,:].==RTm[:,1]-RTm[:,2])

EgressExp = Array{GenericAffExpr, 2}(undef, size(jump,2),npoints)
for p=1:npoints
        #constraints per le propensity#
        k=0;
        for i=1:size(jump,2)
                for j=1:size(jump,2)
                        if(j!=i)
                                k=k+1;
                                @constraint(model,T[k,p]==P[i,j]*Tm[p,i])
                                #salvo l'espressione per il throughput totale di ogni stazione
                                try
                                        EgressExp[i,p]=EgressExp[i,p]+T[k,p]
                                catch
                                        EgressExp[i,p]=@expression(model,T[k,p]+0.0)
                                end
                        end
                end
                @constraint(model,EgressExp[i,p]==Tm[p,i])
        end
        #constraint per lo steady state
        #@constraint(model,jump'*T[:,p].==0)
        @constraint(model,E_abs[p]>=sum(jump'*T[:,p]))
        @constraint(model,E_abs[p]>=-sum(jump'*T[:,p]))
        #constraint per fissare il numero di utenti
        @constraint(model,sum(X[:,p])==Cli[p])
        #per ogni stazione
        for i=1:size(jump,2)
                #constraints per legare il tempo di riposta e il throughput
                @constraint(model,RTs[i,p]==X[i,p]/Tm[p,i])
                #constraints per definire la norma L1 sul tempo di risposta
                #lego le grandezze con la nuova relazione
                @NLconstraint(model,RTlqn[i,p]==sum(P[i,j]*P2[i,j]*RTlqn[i,p] for j=1:size(jump,2))+RTs[i,p])
                @constraint(model,ERT_abs[i,p]>=(RTlqn[i,p]-RTm[p,i]))
                @constraint(model,ERT_abs[i,p]>=(-RTlqn[i,p]+RTm[p,i]))
        end

end


#@objective(model,Min, sum(E_abs2[i,p] for i=1:size(E_abs2,1) for p=1:size(E_abs2,2))+sum(E_abs[i,p] for i=1:size(E_abs,1) for p=1:size(E_abs,2))+sum(ERT_abs[i,p] for i=1:size(ERT_abs,1) for p=1:size(E_abs,2)))
#@objective(model,Min, 0.1*sum(MU)+sum(E_abs[i,p] for i=1:size(E_abs,1) for p=1:size(E_abs,2))+sum(ERT_abs[i,p] for i=1:size(ERT_abs,1) for p=1:size(E_abs,2)))
@objective(model,Min, sum(E_abs)+sum(ERT_abs))
JuMP.optimize!(model)

# matwrite("fromJulia.mat", Dict(
# "RTlqn" => value.(RTlqn),
# "T" => value.(EgressExp),
# "MU" => value.(MU),
# "P" => value.(P),
# "P2" => value.(P.*P2),
# "NCopt" => value.(NC),
# "Cli" => Cli,
# "X" => value.(X)
# );)
