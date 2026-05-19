$已知:dp,dq,p,q,c$<br>

证明:
已知：<br>
${dp}\equiv{d}\pmod{p-1},{dq}\equiv{d}\pmod{q-1}$<br>
$$\because  c^{d}\pmod{N}\equiv{m} \\
\therefore   c^{k(p-1)+dp}\pmod{p}\equiv{m}
$$<br>
$\because$ 欧拉定理<br>
$\therefore$ $c^{k_1(p-1)+dp}\equiv{m}\equiv{c^{dp}}\pmod{p}$<br>
不妨记 ${c}^{dp}\pmod{p}={mp}$<br> 
同理有  $c^{k_2(q-1)+dq}\equiv{m}\equiv{c^{dq}}\pmod{q}$<br>
记 ${c}^{dq}\pmod{q}={mq}$<br>
所以有 $m\equiv{mp}\pmod{p},m\equiv{mq}\pmod{q}$
<br>
根据中国剩余定理
构造 $m$, $m=mp(invert(q,p)q)+mq(invert(p,q)p)\pmod{{p}{q}}$
