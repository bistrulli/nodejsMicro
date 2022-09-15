using NLopt,AmplNLWriter,Couenne_jll,Printf,Ipopt,MadNLP,Plots,MadNLPMumps,JuMP,MAT,ProgressBars,ParameterJuMP,Statistics

mname="acmeAir.py_full"

DATA = matread(@sprintf("../data/%s.mat",mname))

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
#set_optimizer_attribute(model, "linear_solver", "pardiso")
set_optimizer_attribute(model, "max_iter", 20000)
#set_optimizer_attribute(model, "derivative_test", "first-order")
#set_optimizer_attribute(model, "check_derivatives_for_naninf", "yes")

# set_optimizer_attribute(model, "tol", 10^-15)
#set_optimizer_attribute(model, "acceptable_tol", 10^-15)
set_optimizer_attribute(model, "hessian_approximation", "limited-memory")
#set_optimizer_attribute(model, "print_level", 0)

jump=genStoich(size(Tm,2))
npoints=size(RTm,1)

#f(x::T, y::T) where {T<:Real} = -(-x-0+((-x+0)^2+10^-100)^(1.0/2))/2.0
#f(x::T) where {T<:Real} = -(-x+((-x)^2+10^-10)^(1.0/2))/2.0
# function ∇f(g::AbstractVector{T}, x::T, y::T) where {T<:Real}
#     g[1] = 1/2 - (2*x - 2*y)/(4*((x - y)^2 + 1/10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000)^(1/2))
#     g[2] = (2*x - 2*y)/(4*((x - y)^2 + 1/10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000)^(1/2)) + 1/2
#     return
# end
#register(model, :min_, 1, f, autodiff=true) #∇f)

mmu=1 ./minimum(RTm,dims=1)

@variable(model,T[i=1:size(jump,1),j=1:npoints]>=0)
@variable(model,RTlqn[i=1:size(jump,2),p=1:npoints]>=0)

@variable(model,MU[i=1:size(jump,2)]>=0)
@variable(model,X[i=1:size(jump,2),j=1:npoints]>=0)
@variable(model,P[i=1:size(jump,2),j=1:size(jump,2)]>=0)
@variable(model,P2[i=1:size(jump,2),j=1:size(jump,2)]>=0)

@variable(model,E_abs[i=1:(size(jump,2)),j=1:npoints]>=0)
@variable(model,ERT_abs[i=1:size(jump,2),j=1:npoints]>=0)
@variable(model,RTs[i=1:size(jump,2),j=1:npoints]>=0)

@constraint(model,sum(P,dims=2).==1)
#@constraint(model,P2.<=1)
@constraint(model,P.<=1)
@constraint(model,[i=1:size(P2,1)],P2[i,i]==0)

for idx=1:size(MU,1)
        set_start_value(MU[idx],mmu[idx])
        @constraint(model,MU[idx]>=mmu[idx])
end

minExp = Array{NonlinearExpression, 2}(undef, size(jump,2),npoints)
EgressExp = Array{GenericAffExpr, 2}(undef, size(jump,2),npoints)
for p=1:npoints

        #constraints per le propensity#
        k=0;
        for i=1:size(jump,2)
                #mi salvo l'espressione per il min(X[i,p],NC[i,p])
                if(i!=1)
                        minExp[i,p]=@NLexpression(model,(-(-(X[i,p]-NC[p,i])+((-(X[i,p]-NC[p,i]))^2+10^-1)^(1.0/2))/2.0+NC[p,i]))
                else
                        minExp[i,p]=@NLexpression(model,X[i,p]+0.0)
                end
                for j=1:size(jump,2)
                        if(j!=i)
                                k=k+1;
                                @NLconstraint(model,T[k,p]==P[i,j]*MU[i]*minExp[i,p])
                                #println(@sprintf("T[%d,%d]==P[%d,%d]*MU[%d]*X[%d,%d]",k,p,i,j,i,i,p))
                                #salvo l'espressione per il throughput totale di ogni stazione
                                try
                                        EgressExp[i,p]=EgressExp[i,p]+T[k,p]
                                catch
                                        EgressExp[i,p]=@expression(model,T[k,p]+0.0)
                                end
                        end
                end
        end
        #constraint per lo steady state
        @constraint(model,jump'*T[:,p].==0)
        #constraint per fissare il numero di utenti
        @constraint(model,sum(X[:,p])==Cli[p])
        #per ogni stazione
        for i=1:size(jump,2)
                #constraints per legare il tempo di riposta e il throughput
                @NLconstraint(model,EgressExp[i,p]*RTs[i,p]==X[i,p])
                #constraints per definire la norma L1 sul throughput
                @constraint(model,E_abs[i,p]>=(Tm[p,i]-EgressExp[i,p])/Tm[p,i])
                @constraint(model,E_abs[i,p]>=-(Tm[p,i]-EgressExp[i,p])/Tm[p,i])

                #constraints per definire la norma L1 sul tempo di risposta
                #lego le grandezze con la nuova relazione
                @NLconstraint(model,RTlqn[i,p]==sum(P2[i,j]*RTlqn[j,p] for j=1:size(jump,2))+RTs[i,p])
                #@constraint(model,RTlqn[i,p]==sum(P2[i,j]*RTm[p,j] for j=1:size(jump,2))+RTs[i,p])
                @constraint(model,ERT_abs[i,p]>=(RTlqn[i,p]-RTm[p,i])/RTm[p,i])
                @constraint(model,ERT_abs[i,p]>=(-RTlqn[i,p]+RTm[p,i])/RTm[p,i])
        end

end


#@objective(model,Min, sum(E_abs2[i,p] for i=1:size(E_abs2,1) for p=1:size(E_abs2,2))+sum(E_abs[i,p] for i=1:size(E_abs,1) for p=1:size(E_abs,2))+sum(ERT_abs[i,p] for i=1:size(ERT_abs,1) for p=1:size(E_abs,2)))
@objective(model,Min,0.0001*sum(MU)+sum(E_abs[i,p] for i=1:size(E_abs,1) for p=1:size(E_abs,2))+sum(ERT_abs[i,p] for i=1:size(ERT_abs,1) for p=1:size(E_abs,2)))
#@objective(model,Min, sum(E_abs2))
runtime=@elapsed JuMP.optimize!(model)

matwrite(@sprintf("../data/%s_out.mat",mname), Dict(
"RTlqn" => value.(RTlqn),
"T" => value.(EgressExp),
"MU" => value.(MU),
"P" => value.(P),
"P2" => value.(P2),
"NCopt" => value.(NC),
"Cli" => Cli,
"X" => value.(X)
);)
