# coding: utf-8
from enum import Enum
from qfluentwidgets import StyleSheetBase, Theme, isDarkTheme, qconfig
import os
class StyleSheet(StyleSheetBase, Enum):
  """ Style sheet  """

  RECOMMEND_INTERFACE = "recommend_interface"
  CLUSTER_INTERFACE = "recommend_interface"
  PREDICT_INTERFACE = "recommend_interface"
  
  def path(self, theme=Theme.AUTO):
    theme = qconfig.theme if theme == Theme.AUTO else theme
    return os.environ.get('QSS_PATH')+f'\\{theme.value.lower()}\\{self.value}.qss'
    #return f":/gallery/qss/{theme.value.lower()}/{self.value}.qss"
