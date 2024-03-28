"""语言相关类型定义"""

class CTypeBase(object):
    """C语言相关的操作函数＆类型定义"""
    def __init__(self, declare, free_func, encode_func, decode_func):
        self.declare = declare
        self.free_func = free_func
        self.encode_func = encode_func
        self.decode_func = decode_func

"""定义支持的C语言类型"""
CTYPE_OBJS = {
    "boolean": CTypeBase(
        ["gboolean <arg_name>"],
        [],
        ["<arg_out> = g_variant_new_boolean(<arg_name>)"],
        ["<arg_in> = g_variant_get_boolean(<arg_name>)"]
    ),
    "byte": CTypeBase(
        ["guint8 <arg_name>"],
        [],
        ["<arg_out> = g_variant_new_byte(<arg_name>)"],
        ["<arg_in> = g_variant_get_byte(<arg_name>)"]
    ),
    "int16": CTypeBase(
        ["gint16 <arg_name>"],
        [],
        ["<arg_out> = g_variant_new_int16(<arg_name>)"],
        ["<arg_in> = g_variant_get_int16(<arg_name>)"]
    ),
    "uint16": CTypeBase(
        ["guint16 <arg_name>"],
        [],
        ["<arg_out> = g_variant_new_uint16(<arg_name>)"],
        ["<arg_in> = g_variant_get_uint16(<arg_name>)"]
    ),
    "int32": CTypeBase(
        ["gint32 <arg_name>"],
        [],
        ["<arg_out> = g_variant_new_int32(<arg_name>)"],
        ["<arg_in> = g_variant_get_int32(<arg_name>)"]
    ),
    "uint32": CTypeBase(
        ["guint32 <arg_name>"],
        [],
        ["<arg_out> = g_variant_new_uint32(<arg_name>)"],
        ["<arg_in> = g_variant_get_uint32(<arg_name>)"]
    ),
    "int64": CTypeBase(
        ["gint64 <arg_name>"],
        [],
        ["<arg_out> = g_variant_new_int64(<arg_name>)"],
        ["<arg_in> = g_variant_get_int64(<arg_name>)"]
    ),
    "uint64": CTypeBase(
        ["guint64 <arg_name>"],
        [],
        ["<arg_out> = g_variant_new_uint64(<arg_name>)"],
        ["<arg_in> = g_variant_get_uint64(<arg_name>)"]
    ),
    "size": CTypeBase(
        ["gsize <arg_name>"],
        [],
        ["<arg_out> = g_variant_new_uint64(<arg_name>)"],
        ["<arg_in> = g_variant_get_uint64(<arg_name>)"]
    ),
    "ssize": CTypeBase(
        ["gssize <arg_name>"],
        [],
        ["<arg_out> = g_variant_new_int64(<arg_name>)"],
        ["<arg_in> = g_variant_get_int64(<arg_name>)"]
    ),
    "double": CTypeBase(
        ["gdouble <arg_name>"],
        [],
        ["<arg_out> = g_variant_new_double(<arg_name>)"],
        ["<arg_in> = g_variant_get_double(<arg_name>)"]
    ),
    "unixfd": CTypeBase(
        ["gint32 <arg_name>"],
        [],
        ["<arg_out> = g_variant_new_handle(<arg_name>)"],
        ["<arg_in> = g_variant_get_handle(<arg_name>)"]
    ),
    "string": CTypeBase(
        ["<const>gchar *<arg_name>"],
        ["gcl_free_p((void **)&<arg_name>)"],
        ["<arg_out> = gcl_string_encode(<arg_name>)"],
        ["<arg_in> = g_strdup(g_variant_get_string(<arg_name>, NULL))"]
    ),
    "object_path": CTypeBase(
        ["<const>gchar *<arg_name>"],
        ["gcl_free_p((void **)&<arg_name>)"],
        ["<arg_out> = gcl_object_path_encode(<arg_name>)"],
        ["<arg_in> = g_strdup(g_variant_get_string(<arg_name>, NULL))"]
    ),
    "signature": CTypeBase(
        ["<const>gchar *<arg_name>"],
        ["gcl_free_p((void **)&<arg_name>)"],
        ["<arg_out> = gcl_signature_encode(<arg_name>)"],
        ["<arg_in> = g_strdup(g_variant_get_string(<arg_name>, NULL))"]
    ),
    "variant": CTypeBase(
        ["GVariant *<arg_name>"],
        ["gcl_unref_p((GVariant **)&<arg_name>)"],
        ["g_variant_take_ref(<arg_name>)", "<arg_out> = g_variant_new_variant(<arg_name>)"],
        ["<arg_in> = g_variant_get_variant(<arg_name>)"]
    ),
    "array[boolean]": CTypeBase(
        ["gsize n_<arg_name>" ,"<const>gboolean *<arg_name>"],
        ["gcl_free_p((void **)&<arg_name>)"],
        ["<arg_out> = gcl_array_boolean_encode(<arg_name>, n_<arg_name>)"],
        ["<arg_in> = gcl_array_boolean_decode(<arg_name>, &n_<arg_in>)"]
    ),
    "array[byte]": CTypeBase(
        ["gsize n_<arg_name>" ,"<const>guint8 *<arg_name>"],
        ["gcl_free_p((void **)&<arg_name>)"],
        ["<arg_out> = gcl_array_byte_encode(<arg_name>, n_<arg_name>)"],
        ["<arg_in> = gcl_array_byte_decode(<arg_name>, &n_<arg_in>)"]
    ),
    "array[int16]": CTypeBase(
        ["gsize n_<arg_name>" ,"<const>gint16 *<arg_name>"],
        ["gcl_free_p((void **)&<arg_name>)"],
        ["<arg_out> = gcl_array_int16_encode(<arg_name>, n_<arg_name>)"],
        ["<arg_in> = gcl_array_int16_decode(<arg_name>, &n_<arg_in>)"]
    ),
    "array[uint16]": CTypeBase(
        ["gsize n_<arg_name>" ,"<const>guint16 *<arg_name>"],
        ["gcl_free_p((void **)&<arg_name>)"],
        ["<arg_out> = gcl_array_uint16_encode(<arg_name>, n_<arg_name>)"],
        ["<arg_in> = gcl_array_uint16_decode(<arg_name>, &n_<arg_in>)"]
    ),
    "array[int32]": CTypeBase(
        ["gsize n_<arg_name>" ,"<const>gint32 *<arg_name>"],
        ["gcl_free_p((void **)&<arg_name>)"],
        ["<arg_out> = gcl_array_int32_encode(<arg_name>, n_<arg_name>)"],
        ["<arg_in> = gcl_array_int32_decode(<arg_name>, &n_<arg_in>)"]
    ),
    "array[uint32]": CTypeBase(
        ["gsize n_<arg_name>" ,"<const>guint32 *<arg_name>"],
        ["gcl_free_p((void **)&<arg_name>)"],
        ["<arg_out> = gcl_array_uint32_encode(<arg_name>, n_<arg_name>)"],
        ["<arg_in> = gcl_array_uint32_decode(<arg_name>, &n_<arg_in>)"]
    ),
    "array[int64]": CTypeBase(
        ["gsize n_<arg_name>" ,"<const>gint64 *<arg_name>"],
        ["gcl_free_p((void **)&<arg_name>)"],
        ["<arg_out> = gcl_array_int64_encode(<arg_name>, n_<arg_name>)"],
        ["<arg_in> = gcl_array_int64_decode(<arg_name>, &n_<arg_in>)"]
    ),
    "array[uint64]": CTypeBase(
        ["gsize n_<arg_name>" ,"<const>guint64 *<arg_name>"],
        ["gcl_free_p((void **)&<arg_name>)"],
        ["<arg_out> = gcl_array_uint64_encode(<arg_name>, n_<arg_name>)"],
        ["<arg_in> = gcl_array_uint64_decode(<arg_name>, &n_<arg_in>)"]
    ),
    "array[ssize]": CTypeBase(
        ["gsize n_<arg_name>" ,"<const>gssize *<arg_name>"],
        ["gcl_free_p((void **)&<arg_name>)"],
        ["<arg_out> = gcl_array_int64_encode(<arg_name>, n_<arg_name>)"],
        ["<arg_in> = gcl_array_int64_decode(<arg_name>, &n_<arg_in>)"]
    ),
    "array[size]": CTypeBase(
        ["gsize n_<arg_name>" ,"<const>gsize *<arg_name>"],
        ["gcl_free_p((void **)&<arg_name>)"],
        ["<arg_out> = gcl_array_uint64_encode(<arg_name>, n_<arg_name>)"],
        ["<arg_in> = gcl_array_uint64_decode(<arg_name>, &n_<arg_in>)"]
    ),
    "array[double]": CTypeBase(
        ["gsize n_<arg_name>" ,"<const>gdouble *<arg_name>"],
        ["gcl_free_p((void **)&<arg_name>)"],
        ["<arg_out> = gcl_array_double_encode(<arg_name>, n_<arg_name>)"],
        ["<arg_in> = gcl_array_double_decode(<arg_name>, &n_<arg_in>)"]
    ),
    "array[unixfd]": CTypeBase(
        ["gsize n_<arg_name>" ,"<const>gint32 *<arg_name>"],
        ["gcl_free_p((void **)&<arg_name>)"],
        ["<arg_out> = gcl_array_handle_encode(<arg_name>, n_<arg_name>)"],
        ["<arg_in> = gcl_array_handle_decode(<arg_name>, &n_<arg_in>)"]
    ),
    "array[string]": CTypeBase(
        ["gchar * <const>*<arg_name>"],
        ["gcl_strfreev_p(&<arg_name>)"],
        ["<arg_out> = gcl_array_string_encode(<arg_name>)"],
        ["<arg_in> = gcl_array_string_decode(<arg_name>)"]
    ),
    "array[object_path]": CTypeBase(
        ["gchar * <const>*<arg_name>"],
        ["gcl_strfreev_p(&<arg_name>)"],
        ["<arg_out> = gcl_array_object_path_encode(<arg_name>)"],
        ["<arg_in> = gcl_array_object_path_decode(<arg_name>)"]
    ),
    "array[signature]": CTypeBase(
        ["gchar * <const>*<arg_name>"],
        ["gcl_strfreev_p(&<arg_name>)"],
        ["<arg_out> = gcl_array_signature_encode(<arg_name>)"],
        ["<arg_in> = gcl_array_signature_decode(<arg_name>)"]
    )
}