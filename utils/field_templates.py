#!/usr/bin/env python
#
#       field_templates.py
#       

DEFAULT_TEMPLATE = u''' <div class="fieldWrapper">
                            <div class="fieldLabel">%(label)s</div>
                            <div class="fieldInput %(state)s">%(field)s</div>
                            <div class="fieldErrors">%(errors)s</div>
                            <div class="fieldHelp">%(help_text)s</div>
                        </div> 
                    '''
START_TIME_TEMPLATE = u'''<div class="fieldWrapper">
                                <div class="fieldLabel">%(label)s</div>
                                <div class="fieldErrors">%(errors)s</div>
                                <div class="fieldInput %(state)s">%(field)s
                       '''
    
END_TIME_TEMPLATE = u''' To %(field)s</div>
                                <div class="fieldErrors">%(errors)s</div>
                        </div>
                    '''

TIME_TEMPLATE = u'''
              <div class="fieldWrapper">
                <div class="fieldLabel">%(label)s</div>
                <div class="fieldErrors">%(errors)s</div>
                <div class="fieldInput %(state)s">%(start_field)s To %(end_field)s</div>
                <div class="fieldErrors">%(errors)s</div>
              </div>
              '''

ADDONFOOD_GROUP_TEMPLATE = u'''
                                <div class="addonfood">
                                    <div class="fieldLabel">%(label)s</div>
                                    %(field)s
                                    <button type="button" class="add_addon">Add Addon</button>
                                </div>
                            '''

SINGLE_LINE_FIELD = u'''
                       <div class="fieldWrapperFloat">                        
                         <span class="fieldInput %(state)s">%(field)s</span>
                         <span class="fieldErrors">%(errors)s</span>
                       </div> 
                    '''

PASSWORD_FIELD = u'''
                  <div class="fieldWrapperFloat">
                    <input type="text" id="passwordPlaceholder" class="loginInput" tabindex="2" value="Password" />
                    <span class="passInput">%(field)s</span>
                  </div>

                '''
NOTIFY_TEMPLATE = u'''
                    <div class="fieldInput">%(field)s</div>
                    <div class="fieldErrors">%(errors)s</div>
                  '''

REMEMBERME_FIELD = u'''
                <br />%(field)s <span class="headerTxt">%(label)s</span>
              '''
