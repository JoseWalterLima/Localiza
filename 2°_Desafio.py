def horários_livres(agenda, jornada):

    ''' Está função recebe a agenda de uma pessoa - como uma lista de listas -, com os horários de início de fim de cada um de seus 
    compromissos, bem como o horário de início e fim de sua jornada, e retorna todos os intervalos livres dessa pessoa durante o
    dia de trabalho. Caso a jornada comece antes do primeiro compromisso, essa diferença é acrescentada no início dos
    períodos livres. Caso a jornada se encerre após o último compromisso, essa diferença também é acrescentada ao final
    dos períodos livres. A função retorna uma lista de tuplas, onde cada tupla é um intervalo livre.'''

    # Cada elemento da string é transformado em inteiro e depois convertido em minutos. Esse valor é armazenado como inteiro na lista.
    horários_minutos = []
    for compromisso in agenda:
        início_compromisso = (int(compromisso[0].split(':')[0]) * 60) + int(compromisso[0].split(':')[1])
        horários_minutos.append(início_compromisso)
        fim_compromisso = (int(compromisso[1].split(':')[0]) * 60) + int(compromisso[1].split(':')[1])
        horários_minutos.append(fim_compromisso)
    
    # A mesma operação é feita com a jornada de trabalho. Ao final são retornados 2 valores inteiros, referentes aos minutos.
    jornada_minutos = []   
    início_jornada = (int(jornada[0].split(':')[0]) * 60) + int(jornada[0].split(':')[1])
    jornada_minutos.append(início_jornada)
    fim_jornada = (int(jornada[1].split(':')[0]) * 60) + int(jornada[1].split(':')[1])
    jornada_minutos.append(fim_jornada)

    # Para determinar os intervalos livres, é selecionada a hora final de um compromisso e a hora inicial do compromisso subsequente.
    horários_livres = []
    posição = 1 
    while posição < len(horários_minutos[:-1]):
        horários_livres.append(horários_minutos[posição])
        posição += 1
        horários_livres.append(horários_minutos[posição])
        posição += 1

    # Quando um compromisso se inicia exatamente ao final do anterior, o horários ficam duplicados, e precisam ser - ambos - excluídos.
    duplicados = list(set([x for x in horários_livres if horários_livres.count(x) > 1]))
    horários_livres = list(set(horários_livres) - set(duplicados))

    # Caso a jornada se inicie antes dos compromissos, ou encerre após estes, o intervalo precisa ser adicionado aos horários livres.
    if jornada_minutos[0] < horários_minutos[0]:
        horários_livres.append(jornada_minutos[0])
        horários_livres.append(horários_minutos[0])

    if jornada_minutos[1] > horários_minutos[-1]:
        horários_livres.append(jornada_minutos[1])
        horários_livres.append(horários_minutos[-1])

    # A lista final com os horários livres precisa ser colocada em ordem crescente e gerados os pares de oras, como Tuplas. 
    horários_livres.sort()
    hora = iter(horários_livres)
    horários_livres = list(zip(hora, hora))
    return horários_livres


def marcar_reunião(agenda1, jornada1, agenda2, jornada2):
        
        ''' Está função recebe duas agendas, no formato lista de listras, e duas jornadas de trabalho de duas pessoas diferentes, e encontra 
        todos os horários livres possíveis para que estas duas pessoas possam marcar reuniões. A função retorna uma lista de Tuplas, onde
        o primeiro valor é o início do período livre para ambos, e o segundo é o final do período livre para ambos.'''
        
        # A função anterior é aplicada em cada uma das agendas e posteriormente os horários livres são juntados em uma única lista,
        # ordenada pelo primeiro ítem da Tupla.
        lista_final = horários_livres(agenda1, jornada1) + horários_livres(agenda2, jornada2)
        lista_final.sort(key=lambda x: x[0])

        # A cada par de horas é avaliado se o início do horário atual é menor que o final do horário anterior.
        # Em caso positivo, um horário possível é criado, tendo como início o início atual, e como fim o maior valor
        # dentro do intervaldo dos horários finais.
        horários_possíveis = []
        x = 0
        y = 1
        while y < len(lista_final):
                if lista_final[x][1] > lista_final[y][0]:
                        horários_possíveis.append((lista_final[y][0], max(lista_final[x][1], lista_final[y][0])))
                else:
                        pass
                x += 1
                y += 1        

        # Os horários possíveis para as reuniões são transformados para o formato original das agendas.
        horários_possíveis_formatados = []
        for início, fim in horários_possíveis:
                hora_inicial = (início // 60)
                minuto_inicial = (início % 60)
                if minuto_inicial == 0:
                        minuto_inicial = '00'
                início_completo = str(f'{hora_inicial}:{minuto_inicial}')

                hora_final = (fim // 60)
                minuto_final = (fim % 60)
                if minuto_final == 0:
                        minuto_final = '00'
                final_completo = str(f'{hora_final}:{minuto_final}')
                
                marcação = list([início_completo, final_completo])
                
                horários_possíveis_formatados.append(marcação)
        return horários_possíveis_formatados

Agenda_A = [['9:00', '10:30'], ['12:00', '13:00'], ['16:00', '18:00']]
Trabalho_A = ['9:00', '20:00']

Agenda_B = [['10:00', '11:30'], ['12:30', '14:30'], ['14:30', '15:00'], ['16:00','17:00']]
Trabalho_B = ['10:00', '18:30']

print('Considerando a agenda da pessoa A e sua Jornada de Trabalho:')
print(f'Agenda A: {Agenda_A}\nJornada de Trabalho A: {Trabalho_A}')
print('E considerando a agenda da pessoa B e sua Jornada de Trabalho:')
print(f'Agenda B: {Agenda_B}\nJornada de Trabalho B: {Trabalho_B}')
print(f'Os horários possíveis para que eles marquem reuniões são:')
print(marcar_reunião(Agenda_A, Trabalho_A, Agenda_B, Trabalho_B))