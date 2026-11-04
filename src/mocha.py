"""Soft tonal brown controls, with explicit light-surface text colors."""
def soften(theme):
 values={'body_background_fill':'#5C4B40','background_fill_primary':'#E4D4BC','background_fill_secondary':'#C8AF8F','body_text_color':'#2E211B','body_text_color_subdued':'#574435','block_background_fill':'#DCC6A8','block_label_background_fill':'#DCC6A8','block_label_text_color':'#2E211B','block_border_color':'#A88D72','input_background_fill':'#E4D4BC','input_background_fill_focus':'#E4D4BC','input_background_fill_hover':'#E4D4BC','input_placeholder_color':'#574435','input_border_color':'#6E4934','button_primary_background_fill':'#452B1F','button_primary_background_fill_hover':'#6E4934','button_primary_text_color':'#F1E3CD','button_primary_text_color_hover':'#F1E3CD','button_secondary_background_fill':'#C8AF8F','button_secondary_text_color':'#2E211B','error_background_fill':'#DCC6A8','error_text_color':'#2E211B','error_border_color':'#6E4934','loader_color':'#452B1F','link_text_color':'#452B1F'}
 keys=theme.to_dict()['theme'];overrides={}
 for k,v in values.items():
  for variant in [k,k+'_dark']:
   if variant in keys:overrides[variant]=v
 return theme.set(**overrides)
