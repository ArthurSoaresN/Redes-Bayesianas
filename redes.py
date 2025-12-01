# Redes -> Furto ou Terremoto

bn = AdapterBayesNet()
bn.add('Burglary', '', 0.001)
bn.add('Earthquake', '', 0.002)
bn.add('Alarm', 'Burglary Earthquake', {
        (T, T): 0.95,
        (T, F): 0.94,
        (F, T): 0.29,
        (F, F): 0.001,
    })
bn.add('JohnCalls', 'Alarm', {T: 0.90, F: 0.05})
bn.add('MaryCalls', 'Alarm', {T: 0.70, F: 0.01})

dist = enumeration_ask('Burglary', {'JohnCalls': T, 'MaryCalls': T}, bn)
print('Adapter P(B|J,M)=', dist[T])  # ≈ 0.2841718353643929
print('Adapter P(B|J,M)=', dist[F])

# ==================================================
# Redes -> Desempenho nas provas

pv = AdapterBayesNet()
pv.add('Prova', '', {'facil': 0.6, 'dificil': 0.4})
pv.add('Qi', '', {'alto': 0.3, 'baixo': 0.7})
pv.add('Nota', 'Prova Qi', {
        ('facil', 'alto'): {'nota alta': 0.9, 'nota media': 0.09, 'nota baixa': 0.01},
        ('dificil', 'alto'): {'nota alta': 0.5, 'nota media': 0.3, 'nota baixa': 0.2},
        ('facil', 'baixo'): {'nota alta': 0.3, 'nota media': 0.6, 'nota baixa': 0.1},
        ('dificil', 'baixo'): {'nota alta': 0.01, 'nota media': 0.09, 'nota baixa': 0.9}
})
pv.add('Aprovado', 'Nota', {'nota alta': 0.9, 'nota media': 0.6, 'nota baixa': 0.01})

# Qual é a probabilidade de um estudante ter tirado nota alta, dado que ele foi aprovado?

resultado = enumeration_ask('Nota', {'Aprovado': T}, pv)
print('\nQual é a probabilidade de um estudante ter tirado nota alta, dado que ele foi aprovado?')
print(f'1. Adapter P(Nota Alta | Aprovação) = {resultado["nota alta"]:.4f}')

# Qual é a probabilidade da prova ter sido difícil, dado que o estudante tirou nota baixa?.

resultado2 = enumeration_ask('Prova', {'Nota': 'nota baixa'}, pv)
print('\nQual é a probabilidade da prova ter sido difícil, dado que o estudante tirou nota baixa?')
print(f'1. Adapter P(Prova Dificil | Nota Baixa) = {resultado2["dificil"]:.4f}')

# Qual é a probabilidade de um estudante ter QI baixo, dado que ele tirou uma nota alta e a prova foi difícil?.

resultado3 = enumeration_ask('Qi', {'Nota': 'nota alta', 'Prova': 'dificil'}, pv)
print('\nQual é a probabilidade de um estudante ter QI baixo, dado que ele tirou uma nota alta e a prova foi difícil?')
print(f'1. Adapter P(Qi Baixo | Nota Alta, Prova Dificil) = {resultado3["baixo"]:.4f}')

# ==================================================
# Redes -> Clima para picnic

wx = AdapterBayesNet()
wx.add('Weather', '', {'sunny': 0.6, 'rainy': 0.3, 'cloudy': 0.1})
wx.add('Picnic', 'Weather', {
        ('sunny',): {'go': 0.9, 'stay': 0.1},
        ('rainy',): {'go': 0.2, 'stay': 0.8},
        ('cloudy',): {'go': 0.6, 'stay': 0.4},
    })

print('Adapter P(Weather)=', enumeration_ask('Weather', {}, wx).prob)
print('Adapter P(Weather|Picnic=stay)=', enumeration_ask('Weather', {'Picnic': 'stay'}, wx).prob)

#ou

print('\nAdapter P(Weather)=')
pw = enumeration_ask('Weather', {}, wx)
print('', pw.show_approx())
pw.show_approx()


print('\nAdapter P(Weather|Picnic=stay)=')
pw2 = enumeration_ask('Weather', {'Picnic': 'stay'}, wx)
pw2.show_approx()

# ==================================================
# Redes -> Bonus do codigo

cd = AdapterBayesNet()
cd.add('Complexidade', '', {'simples': 0.7, 'complexo': 0.3})
cd.add('Nivel', '', {'senior': 0.4, 'junior': 0.6})

cd.add('Qualidade', 'Nivel Complexidade', {
    ('senior', 'simples'): {'limpo': 0.95, 'usavel': 0.04, 'bugado': 0.01},
    ('senior', 'complexo'): {'limpo': 0.60, 'usavel': 0.30, 'bugado': 0.10},
    ('junior', 'simples'): {'limpo': 0.40, 'usavel': 0.50, 'bugado': 0.10},
    ('junior', 'complexo'): {'limpo': 0.05, 'usavel': 0.25, 'bugado': 0.70}
})

cd.add('Bonus', 'Qualidade', {'limpo': 0.9, 'usavel': 0.5, 'bugado': 0.05})

resultado1 = enumeration_ask('Qualidade', {'Bonus': T}, cd)
print('\n1. Qual a probabilidade de um projeto ter tido código "Limpo", dado que o time ganhou o Bônus?')
print(f'R: {resultado1["limpo"]:.4f}')

# Q2: Probabilidade do projeto ser "Complexo", dado que o código saiu "Bugado"?
resultado2 = enumeration_ask('Complexidade', {'Qualidade': 'bugado'}, cd)
print('\n2. Qual a probabilidade do projeto ser "Complexo", dado que o código saiu "Bugado"?')
print(f'R: {resultado2["complexo"]:.4f}')

# Q3: Probabilidade do desenvolvedor ser "Junior", dado código "Limpo" em projeto "Complexo"?
resultado3 = enumeration_ask('Nivel', {'Qualidade': 'limpo', 'Complexidade': 'complexo'}, cd)
print('\n3. Qual a probabilidade do desenvolvedor ser "Junior", dado que ele entregou código "Limpo" em um projeto "Complexo"?')
print(f'R: {resultado3["junior"]:.4f}')