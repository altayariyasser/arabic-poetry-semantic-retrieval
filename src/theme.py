"""Set identical light/dark tokens using only keys present in installed Gradio."""
TOKENS={'ivory':'#FAF7F2','cream':'#F1E8DA','coffee':'#452B1F','walnut':'#6E4934','caramel':'#A7754F','border':'#DDCBB7','text':'#2E211B','muted':'#69564B','white':'#FFFFFF'}
def make_theme():
 import gradio as gr
 c=TOKENS;t=gr.themes.Base(font=['Tahoma','Arial','sans-serif'],font_mono=['Tahoma'])
 values={
 'body_background_fill':c['ivory'],'background_fill_primary':c['ivory'],'background_fill_secondary':c['cream'],'body_text_color':c['text'],'body_text_color_subdued':c['muted'],
 'block_background_fill':c['white'],'block_border_color':c['border'],'block_label_background_fill':c['white'],'block_label_text_color':c['text'],'block_title_text_color':c['coffee'],
 'input_background_fill':c['white'],'input_background_fill_focus':c['white'],'input_background_fill_hover':c['white'],'input_border_color':c['walnut'],'input_border_color_focus':c['coffee'],'input_border_color_hover':c['coffee'],'input_placeholder_color':c['muted'],
 'button_primary_background_fill':c['coffee'],'button_primary_background_fill_hover':c['walnut'],'button_primary_border_color':c['coffee'],'button_primary_border_color_hover':c['walnut'],'button_primary_text_color':c['white'],'button_primary_text_color_hover':c['white'],
 'button_secondary_background_fill':c['cream'],'button_secondary_background_fill_hover':c['white'],'button_secondary_text_color':c['coffee'],'button_secondary_text_color_hover':c['coffee'],'button_secondary_border_color':c['walnut'],
 'error_background_fill':c['cream'],'error_border_color':c['walnut'],'error_text_color':c['text'],'error_icon_color':c['coffee'],
 'border_color_primary':c['border'],'border_color_accent':c['coffee'],'border_color_accent_subdued':c['walnut'],'panel_background_fill':c['cream'],'panel_border_color':c['border'],
 'link_text_color':c['walnut'],'link_text_color_hover':c['coffee'],'link_text_color_active':c['coffee'],'link_text_color_visited':c['walnut'],'loader_color':c['coffee'],
 'checkbox_label_background_fill':c['white'],'checkbox_label_background_fill_selected':c['cream'],'checkbox_label_background_fill_hover':c['cream'],'checkbox_border_color':c['walnut'],'checkbox_border_color_focus':c['coffee'],'checkbox_border_color_selected':c['coffee'],
 'code_background_fill':c['cream'],'table_even_background_fill':c['white'],'table_odd_background_fill':c['cream']}
 available=t.to_dict()['theme'];safe={}
 for key,value in values.items():
  for variant in [key,key+'_dark']:
   if variant in available:safe[variant]=value
 return t.set(**safe)
