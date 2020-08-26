# def convert_u_int64_to_int64(u_int_64number):
#
#
#     if (u_int_64number & 0x80000000) == 0x80000000:
#         signed_1_s_complement = u_int_64number ^ 0xffffffff
#         signed_2_s_complement = (signed_1_s_complement + 1) * -1
#         print("signed_2_s_complement {}".format(signed_2_s_complement))
#         return signed_2_s_complement
#     elif (u_int_64number & 0x80000000) == 0x00000000:
#         print("u_int_64number {}".format(u_int_64number))
#         return u_int_64number
#     else:
#         print("error")
#
#
# def handle_exception_of_convert_u_int64_to_int64(u_int_64number):
#     try:
#         convert_u_int64_to_int64(u_int_64number)
#     except TypeError:
#         print("be sure to give an hexadecimal number in u_int_64number")
#
#
# handle_exception_of_convert_u_int64_to_int64(u_int_64number=0x80000000)
