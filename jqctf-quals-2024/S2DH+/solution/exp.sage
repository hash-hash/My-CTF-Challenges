from Crypto.Cipher import AES
from hashlib import md5

N1 = 5**32
N2 = 542101086261801844455116495407706582706462721
g = 296
p = g*N1*N2-1

K.<i> = GF(p^2, modulus=x^2+1)
E0 = EllipticCurve(K, [1, 0])

Pa, Qa = ((1108151264392167107399079845392167260393119570395824057352377785487704*i + 3070928543118575318205521100703992179773098148088303610394443246633078, 3418584656719813748421123105175064398106405727751395507158710618133606*i + 2264837070461895881762205550619004445139150452039141410498701490352565), (3657567537645797599941562162026529235773040822594922004793160804533978*i + 2751967678367936106930385919452698226182000199114268439990801739325018, 1833413950720975506311986972905072224314149393183031888315051658688737*i + 1911352306422552638655963844259232499638220906121724668024928926413255))
Pb, Qb = ((3669477050200737811937605490576620857420084147322274766489781462625295*i + 1197668251702966592048224829615867575845382005843213964433434027982049, 1424041143351434937659195965628444352658127009880329906348989041068271*i + 1177757638754703040664378142633763467467820174229896310077131953049364), (1587585227440205348532344742508247573159306595269236493411455740945798*i + 322704997598463265822546451892473977913451923495875397197941568334653, 328752559941607854463085252260936323498890994438786191738866959445311*i + 1811355937590183765257326376837022825123649909604461212098307111812867))
a4, a6, phiPb, phiQb = (2502746812469053334365157968619353919833571073472295217502172818828605*i + 3500462226854593815830739241199402224087760112765329748785541540975263, 2749102118331842791128930717108118236427449938819264040239390644820541*i + 764563719463454893299096262812503543049739927289729724450069493046310, (298939841279086756220738341004823798548640535647088497975783258562088*i + 3595957781725923780378348304680941457076679477390991867267087073504780, 3058250341065191646817754784970161544054286076887979215384902280165328*i + 2900806682779300248162620222889861698236496381389106684202107340044202), (2383914257081985239023160010762140274690332456784572329606402861569789*i + 2616075158850761045048996394509986318086044946946891379813162349332054, 2253827048633979689644503970472332098460301422297773437353706000601491*i + 1379677649946979530392361025346222099538941934061143670463467042820345))
b4, b6, psiPa, psiQa = (436201707373323048881717452193137631315319220455328489177684037008824*i + 684580438385891039988125331016218753118547820701790758611586264146402, 309799667936414863572925101343703961075294778416611666637534968929551*i + 1119807000673888381491604797666929470642053526207914386502196360088420, (1129907168532387101087143768078125604591095362816083257109272335012068*i + 1849017000528591493758889211435235771210593091988571829711315364645753, 2022857255509405860197809751670228342541913649124883104695127465945964*i + 408090949105464775634096515968960854952554380711163802247061022458654), (1473398142465675988025320987931070759327208010586033939272763907565391*i + 608508276993122453949815530124658002751535507998356995878173870973722, 3203033302636493762386558138531367968019399303394849127325409518541880*i + 1945513955640192864557418105118230330586406149943003356310032147090738))
c = bytes.fromhex('f61ab0dd10e04c84a855e160cdae798211b87e73992f9a36657377d63564ed468d887b3bc0dd24593044ca70fa6f6082')

Ea = EllipticCurve(K, [a4, a6])
Eb = EllipticCurve(K, [b4, b6])

d = isqrt(N2-N1^2)
assert N1^2+d^2 == N2

def theta(P):
    x, y = P.xy()
    x = -x; y = i*y
    return E0(x, y)

Pb, Qb = E0(Pb), E0(Qb)
phiPb, phiQb = Ea(phiPb), Ea(phiQb)

Pb_ = theta(N1*Pb)
Qb_ = theta(N1*Qb)

def elog(R, P, Q):
    g = P.weil_pairing(Q, N2)
    n = g.multiplicative_order()
    y1 = R.weil_pairing(P, N2)
    y2 = R.weil_pairing(Q, N2)
    y0 = n-y1.log(g)
    x0 = y2.log(g)
    assert R == x0*P+y0*Q
    return x0, y0

x0, y0 = elog(Pb_, Pb, Qb)
x1, y1 = elog(Qb_, Pb, Qb)
TPb = x0*phiPb+y0*phiQb+d*phiPb
TQb = x1*phiPb+y1*phiQb+d*phiQb
ker_s = N2-TQb.discrete_log(TPb)

comphi = Ea.isogeny(ker_s*phiQb+phiPb, algorithm="factored")
dscalar = Ea.scalar_multiplication(d)
iso = comphi.codomain().isomorphism_to(Ea)
iso_ = Ea.isomorphism_to(Ea)
comphi = iso_*iso*comphi

basis = Ea.torsion_basis(N1)
basis1 = comphi(basis[0])-dscalar(basis[0])
basis2 = comphi(basis[1])-dscalar(basis[1])
sk = N1-basis2.discrete_log(basis1)

comphi_ = Ea.isogeny(basis[0]+sk*basis[1], algorithm="factored")
iso2 = comphi_.codomain().isomorphism_to(E0)
phi = iso2*comphi_
phi_ = -phi.dual()
phiPa = phi_(Pa)
phiQa = phi_(Qa)
ska = (-phiQa).discrete_log(phiPa)

key = md5(str(ska).encode()).digest()
m = AES.new(key, AES.MODE_ECB).decrypt(c)
print(m)