class CLASS_EMPTY:
	pass

INSTANCE_EMPTY = CLASS_EMPTY()

reference_CLASS = vars(CLASS_EMPTY)
reference_INSTANCE = vars(INSTANCE_EMPTY)



def FilterClassNames(source):
	return {k:v for (k,v) in vars(source).items() if k not in reference_CLASS}



mask_handle = 0xFFFF00
def Handle(instance):
	n = id(instance)
	h = (n & mask_handle) >> 8
	l = n & (~mask_handle & 0XFFFFFF)
	return f'0x{h:04X} {l:02X}'
