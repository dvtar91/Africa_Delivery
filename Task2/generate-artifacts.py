#!/usr/bin/env python3
"""Rebuild Task2 binary deliverables in GitHub CI; assumptions are NOT vendor quotes."""
from pathlib import Path
import subprocess
import xlsxwriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor as C

ROOT = Path(__file__).resolve().parent
assumptions = {
    "basket": 25, "orders_user": 2.4, "psp": .024, "shipping": 1.2,
    "messages": .035, "infra_growth": .13, "wage_growth": .06,
    "inflation": .04, "discount": .15, "contractor": 3500,
    "compliance_y1": 20000, "compliance_y2": 7000,
    "loss_min": 12000, "slo_scenario": .995, "cfo_cap": 5000
}
scenarios = [('A Монолит',2600,6,6000,50000),('B Сервисы',4700,9,18000,100000),
             ('C CTO',18500,18,80000,250000)]
users = [50000,120000,250000,500000,1000000]
workbook=xlsxwriter.Workbook(str(ROOT/'tco-model.xlsx'))
hd=workbook.add_format({'bold':True,'font_color':'white','bg_color':'#17324D','text_wrap':True})
num=workbook.add_format({'num_format':'#,##0.00'})
pct=workbook.add_format({'num_format':'0.0%'})
note=workbook.add_format({'text_wrap':True,'font_color':'#475569'})
a=workbook.add_worksheet('Допущения')
a.set_column('A:A',37);a.set_column('B:B',20);a.set_column('C:C',20);a.set_column('D:D',70)
a.write_row('A1',['Параметр','Значение','Единица','Комментарии'],hd)
items=[
 ('Средний чек',25,'USD','Допущение'),('Заказов на пользователя',2.4,'шт/год','Условное'),
 ('PSP с конвертацией',.024,'доля GMV','Порог CFO строго ниже 2,5%, тариф не подтверждён'),
 ('Логистика на заказ',1.2,'USD','Платформенная часть, не вся перевозка'),
 ('Сообщения на заказ',.035,'USD','Только с правовым основанием'),
 ('Рост инфраструктуры',.13,'доля','Модель'),('Рост ФОТ',.06,'доля','Модель'),
 ('Инфляция',.04,'доля','Модель'),('Ставка дисконтирования',.15,'доля','Модель'),
 ('FTE в месяц',3500,'USD','Условная полная стоимость контрактора'),
 ('Compliance Y1',20000,'USD','Оценка'),('Compliance Y2+',7000,'USD','Оценка'),
 ('Потеря / мин',12000,'USD','Слова инвестора, НЕ подтверждённая прибыль'),
 ('SLO сценарий',.995,'доля','Не соглашение'),('CFO лимит',5000,'USD/мес','Первые 6 месяцев')]
for i,row in enumerate(items,1):a.write_row(i,0,row)
a.write_row('A19',['Год','Y1','Y2','Y3','Y4','Y5'],hd)
a.write('A20','Пользователи');a.write_row('B20',users)
a.write('A21','Заказы');a.write('A22','GMV')
for y in range(5):
 col=xlsxwriter.utility.xl_col_to_name(y+1)
 a.write_formula(20,y+1,f'={col}20*$B$3',num)
 a.write_formula(21,y+1,f'={col}21*$B$2',num)
a.write('A24','Все тарифы гипотетические, не договорные; input Task1 C-01/C-07.')
a.freeze_panes(1,1)
for name,base,fte,setup,scale in scenarios:
 s=workbook.add_worksheet(name);s.set_column('A:A',49);s.set_column('B:F',19);s.freeze_panes(3,1)
 s.write('A1',name+' | TCO 5 лет (USD)',hd)
 s.write_row('A3',['Показатель','Y1','Y2','Y3','Y4','Y5'],hd)
 lab={4:'Пользователи',5:'Заказы',6:'GMV',8:'Infra + SaaS',9:'Команда/FTE',10:'PSP+FX',11:'Доставка',12:'Уведомления',13:'Compliance',14:'Внедрение',15:'Всего TCO',16:'Технические расходы (infra+люди+legal+setup)',17:'TCO / заказ',18:'Tech cost / заказ',19:'NPV годовой',21:'TCO 5 лет',22:'NPV 5 лет',23:'Стоимость заказа за 5 лет',24:'Избыточные fixed costs относительно A за 5 лет',25:'Monthly infra+SaaS при старте',26:'CFO cap (1=pass)',27:'FTE',28:'Плановая цена миграции к 10M (НЕ baseline)',30:'SLO стресс-допущение',31:'Минут простоя при SLO / год',32:'Гипотетические потери / год',33:'TCO с условной стоимостью простоя'}
 for row,txt in lab.items():s.write(row-1,0,txt)
 for y in range(5):
  col=xlsxwriter.utility.xl_col_to_name(y+1)
  formulas={4:f"='Допущения'!{col}20",5:f"='Допущения'!{col}21",6:f"='Допущения'!{col}22",
   8:f"={base}*12*(1+'Допущения'!$B$7)^{y}",
   9:f"={fte}*'Допущения'!$B$11*12*(1+'Допущения'!$B$8)^{y}",
   10:f"={col}6*'Допущения'!$B$4",11:f"={col}5*'Допущения'!$B$5",
   12:f"={col}5*'Допущения'!$B$6",
   13:"='Допущения'!$B$12" if y==0 else f"='Допущения'!$B$13*(1+'Допущения'!$B$9)^{y}",
   15:f'=SUM({col}8:{col}14)',16:f'={col}8+{col}9+{col}13+{col}14',
   17:f'={col}15/{col}5',18:f'={col}16/{col}5',
   19:f"={col}15/(1+'Допущения'!$B$10)^{y+1}",
   30:"='Допущения'!$B$15",31:f'=(1-{col}30)*365*24*60',
   32:f"={col}31*'Допущения'!$B$14",33:f'={col}15+{col}32'}
  for row,f in formulas.items():s.write_formula(row-1,y+1,f,num)
  s.write(13,y+1,setup if y==0 else 0,num)
 s.write_formula('B21','=SUM(B15:F15)',num)
 s.write_formula('B22','=SUM(B19:F19)',num)
 s.write_formula('B23','=B21/SUM(B5:F5)',num)
 # Fixed overhead relative to A at identical user volume, not an accounting write-off
 s.write_formula('B24',f'=SUM(B8:F9)+SUM(B13:F14)-SUM(31200*(1+\'Допущения\'!$B$7)^0,31200*(1+\'Допущения\'!$B$7)^1,31200*(1+\'Допущения\'!$B$7)^2,31200*(1+\'Допущения\'!$B$7)^3,31200*(1+\'Допущения\'!$B$7)^4)-SUM(252000*(1+\'Допущения\'!$B$8)^0,252000*(1+\'Допущения\'!$B$8)^1,252000*(1+\'Допущения\'!$B$8)^2,252000*(1+\'Допущения\'!$B$8)^3,252000*(1+\'Допущения\'!$B$8)^4)-20000-4*7000-6000',num)
 s.write_formula('B25','=B8/12',num)
 s.write_formula('B26',"=IF(B25<='Допущения'!$B$16,1,0)")
 s.write('B27',fte);s.write('B28',scale)
 s.write('A35','Сценарий 50k: неизменные 50k пользователей все 5 лет; B24 = difference in fixed overhead vs A.',note)
 s.write('A36','Сценарий 10M: резерв B28 не включён в baseline; нужна проверка нагрузки и коммерческих тарифов.',note)
 s.write('A37','TCO и потери при SLO показаны отдельно, без смешения cash cost с модельным ущербом.',note)
workbook.close()

FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
pdfmetrics.registerFont(TTFont('DejaVu',FONT));pdfmetrics.registerFont(TTFont('DejaVuBold',BOLD))
c=canvas.Canvas(str(ROOT/'nairobi-slide..pdf'),pagesize=(960,540))
c.setFillColor(C('#12273B'));c.rect(0,0,960,540,fill=1,stroke=0)
c.setFillColor(C('#8DDEF2'));c.setFont('DejaVuBold',13);c.drawString(48,493,'AFRICA DELIVERY  /  NAIROBI  /  ARCHITECTURE DECISION')
c.setFillColor(C('#FFFFFF'));c.setFont('DejaVuBold',26);c.drawString(48,444,'Модульный монолит — управляемый MVP')
c.setFont('DejaVu',13);c.drawString(48,414,'Решение условное: CFO, CTO, CEO, Legal и инвестор должны согласовать gates')
for i,(title,weeks,cost,fte,col) in enumerate([
 ('A  МОДУЛЬНЫЙ МОНОЛИТ','8–10 недель','$2 600/мес.','6 FTE','#167D8D'),
 ('B  5–7 СЕРВИСОВ','14–18 недель','$4 700/мес.','9 FTE','#314F69'),
 ('C  CTO: 40 СЕРВИСОВ','28–40 недель','$18 500/мес.','18 FTE','#6E3D49')]):
 x=46+i*306;c.setFillColor(C(col));c.roundRect(x,245,288,138,12,fill=1,stroke=0)
 c.setFillColor(C('#FFFFFF'));c.setFont('DejaVuBold',13);c.drawString(x+15,352,title)
 c.setFont('DejaVu',14);c.drawString(x+15,319,weeks)
 c.setFont('DejaVuBold',17);c.drawString(x+15,283,cost)
 c.setFont('DejaVu',13);c.drawString(x+210,257,fte)
c.setFillColor(C('#83D8B9'));c.setFont('DejaVuBold',15);c.drawString(48,213,'ПОЧЕМУ A: $5 000/мес. техлимит · максимум 6 контракторов')
c.setFillColor(C('#E8F1F5'));c.setFont('DejaVu',12)
for i,line in enumerate([
 'Работоспособный заказ → PSP → партнёрская доставка → сверка и возврат.',
 'Не строим до спроса: Oracle, Kafka, Istio, 3 K8s, собственный logistics engine.',
 'GATES: legal/data · PSP fee < 2,5% GMV · возвраты · языки · scope рекламы.']):
 c.drawString(48,170-i*25,line)
c.setFont('DejaVu',10);c.drawString(48,54,'Цифры — инженерные допущения, не котировки. 15.10.2026 — прошедшая дата.')
c.drawString(48,35,'Источники: Task1 / options-comparison / tco-model / ADR-001')
c.showPage();c.save()
graphs={
'c4-context.png':'''digraph G {graph [rankdir=LR,fontsize=14,fontname="DejaVu Sans"];node [shape=box,style="rounded,filled",fillcolor="#E3EFF7",fontname="DejaVu Sans"];Buyer [label="Покупатель"];Seller [label="Продавец"];Ops [label="Оператор"];CEO [label="CEO/CFO"];System [label="Africa Delivery\\nMVP",fillcolor="#277D98",fontcolor=white];MP [label="M-Pesa"];FW [label="Flutterwave"];PS [label="Paystack"];SB [label="Sendbox"];SY [label="Sendy"];WA [label="WhatsApp Business API"];SMS [label="SMS/USSD gateway"];Buyer->System [label="заказ/статус"];Seller->System [label="товары/KYB"];Ops->System [label="возврат/сверка"];CEO->System [label="KPI"];System->MP [label="платёж+webhook"];System->FW [label="платёж+webhook"];System->PS [label="PSP при договоре"];System->SB [label="доставка"];System->SY [label="доставка"];System->WA [label="opt-in уведомления"];System->SMS [label="SMS; USSD gate"]; }''',
'use-cases.png':'''digraph G {graph [rankdir=LR,fontname="DejaVu Sans"];node [shape=ellipse,style=filled,fillcolor="#E3EFF7",fontname="DejaVu Sans"];Buyer [shape=box,label="Покупатель"];Seller [shape=box,label="Продавец"];Ops [shape=box,label="Оператор"];CEO [shape=box,label="CEO / CFO"];Buyer->Catalog [label="просмотр каталога"];Buyer->Checkout [label="оформить заказ"];Buyer->Pay [label="оплатить через PSP"];Buyer->Track [label="статус доставки"];Buyer->Return [label="возврат"];Seller->KYB [label="верификация"];Seller->SKU [label="разместить SKU"];Seller->Payout [label="выплаты"];Ops->Moderate [label="модерация"];Ops->Refund [label="refund"];Ops->Reconcile [label="сверка PSP"];CEO->KPI [label="оперативный отчёт"];Pay->Reconcile [style=dashed,label="webhook"];Return->Refund [style=dashed,label="обработка"]; }''' }
for out,dot in graphs.items():
 p=ROOT/(out+'.dot');p.write_text(dot,encoding='utf8')
 subprocess.run(['dot','-Tpng',str(p),'-o',str(ROOT/out)],check=True)
print('Generated:',*[str(ROOT/x) for x in ['tco-model.xlsx','nairobi-slide..pdf','c4-context.png','use-cases.png']])
