#include "gcl_base.h"
#include "${intf.name}.h"

<%
class_name = intf.alias
properties = "_" + class_name + "_properties"
signal_processer = "_" + class_name + "_signals"
%>\
static ${class_name}_Properties ${properties};
static const ${class_name}_Signals *${signal_processer} = NULL;

% for prop in intf.properties:
/* ${prop.description} */
    % if prop.deprecated:
__attribute__((__deprecated__)) void ${class_name}_set_${prop.name}(const ${class_name} *object,
    ${", ".join(prop.declare()).replace("<arg_name>", "value").replace("<const>", "const ")})
    % else:
void ${class_name}_set_${prop.name}(const ${class_name} *object,
    ${", ".join(prop.declare()).replace("<arg_name>", "value").replace("<const>", "const ")})
    % endif
{
    GVariant *tmp = NULL;
    % for line in prop.encode_func():
    ${line.replace("<arg_out>", "tmp").replace("n_<arg_name>", "n_value").replace("<arg_name>", "value")};
    % endfor
    gcl_set_value((GclObject *)object, &_${class_name}_properties.${prop.name}, tmp);
    g_variant_unref(tmp);
}

% endfor
% for signal in intf.signals:
/*
 * Signal: ${signal.name}
 * ${signal.description}
 */
    % if signal.deprecated:
__attribute__((__deprecated__)) gboolean ${class_name}_${signal.name}_Signal(const ${class_name} *object,
    const gchar *destination, const ${class_name}_${signal.name}_Msg *msg, GError **error)
    % else:
gboolean ${class_name}_${signal.name}_Signal(const ${class_name} *object, const gchar *destination,
    const ${class_name}_${signal.name}_Msg *msg, GError **error)
    % endif
{
    if (error == NULL) {
        log_error("Emit ${signal.name} with parameter error, error is NULL");
        return FALSE;
    }
    if (object == NULL) {
        *error = g_error_new(G_DBUS_ERROR, G_DBUS_ERROR_FAILED, "Emit ${signal.name} with parameter error, object is NULL");
        return FALSE;
    }
    return gcl_impl.emit_signal((GclObject *)object, destination,
        (const GclSignal *)&${signal_processer}->${signal.name}, msg, error);
}

% endfor
static GclObject *_${class_name}_create(const gchar *obj_name, gpointer opaque);
/*
 * interface: ${intf.name}
% for c in intf.description.split("\n"):
 * ${c}
% endfor
 */
static GclInterface _${class_name}_interface = {
    .create = _${intf.alias}_create,
    .is_remote = 0,
    .name = "${intf.name}",
    .properties = (GclProperty *)&${properties},
    .interface = NULL,  /* load from usr/share/dbus-1/interfaces/${intf.name} by gcl_init */
};

/**
 * @brief 分配对象
 *
 * @param obj_name 对象名，需要由调用者分配内存
 * @param opaque 上层应用需要写入对象的用户数据，由上层应用使用
 */
GclObject *_${class_name}_create(const gchar *obj_name, gpointer opaque)
{
    ${class_name} *obj = g_new0(${class_name}, 1);
    memcpy(obj->_base.magic, GCL_MAGIC, strlen(GCL_MAGIC) + 1);
    obj->_base.lock = g_new0(GRecMutex, 1);
    g_rec_mutex_init(obj->_base.lock);
    obj->_base.name = obj_name;
    obj->_base.intf = &_${class_name}_interface;
    obj->_base.opaque = opaque;
    return (GclObject *)obj;
}

GclInterface *${class_name}_interface(void)
{
    return &_${class_name}_interface;
}

${class_name}_Properties *${class_name}_properties(void)
{
    return &${properties};
}

static void __attribute__((constructor(150))) ${class_name}_register(void)
{
    // 从公共库中复制信号处理函数
    ${signal_processer} = ${class_name}_signals();
    // 从公共库中复制方法处理函数
    _${class_name}_interface.methods = (GclMethod *)${class_name}_methods();
    _${class_name}_interface.signals = (GclSignal *)${class_name}_signals();

    // 从公共库中复制属性信息
    memcpy(&${properties}, ${class_name}_properties_const(), sizeof(${properties}));
    gcl_interface_register(&_${class_name}_interface,
                           "${intf.introspect_xml_sha256}",
                           "/usr/share/dbus-1/interfaces/${intf.name}.xml");
}
