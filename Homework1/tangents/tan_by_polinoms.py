import math

def polinomial_tan(x):
 const1 = 0.33333333333333333
 const2 = 0.133333333333333333
 const3 = 0.053968253968254
 const4 = 0.0218694885361552

 x_2nd = x * x
 x_3rd = x_2nd * x
 x_5th = x_3rd * x_2nd
 x_7th = x_5th * x_2nd
 x_9th = x_7th * x_2nd

 poli_tan = x + const1 * x_3rd + const2 * x_5th + const3 * x_7th + const4 * x_9th

 return poli_tan

def better_polinomial_tan(x):

 was_normalized = False
 is_x_negative = False

 if x > math.pi/4 or x < (-1)*math.pi/4:
  is_x_negative = x < 0
  x = abs(x)
  x = (math.pi/2) - x
  was_normalized = True

 poli_tan = polinomial_tan(x)

 if was_normalized:
  new_poli_tan = 1.0 / poli_tan
  if is_x_negative:
   return new_poli_tan * (-1)
  else:
   return new_poli_tan
 else:
  return poli_tan