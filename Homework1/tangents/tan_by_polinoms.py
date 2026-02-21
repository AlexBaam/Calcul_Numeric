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
