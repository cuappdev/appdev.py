from base_controller import *
from flask import jsonify
import abc

# A REST-API controller that handles boilerplate for
# serving up JSON responses based on HTTP verbs
class AppDevController(BaseController):
  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def content(self, **kwargs):
    return dict()

  def get_name(self):
    return self.get_path().replace('/', '-')

  def response(self, **kwargs):
    content = self.content(**kwargs)
    try:
      return jsonify({
        'success': True,
        'data': content
      })
    except Exception as e:
      print e
      return jsonify({
        'success': False,
        'data': { 'errors': [str(e)] }
      })
