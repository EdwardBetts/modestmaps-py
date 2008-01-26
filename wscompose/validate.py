# -*-python-*-

__package__    = "wscompose/validate.py"
__version__    = "1.0"
__author__     = "Aaron Straup Cope"
__url__        = "http://www.aaronland.info/python/wscompose"
__date__       = "$Date: 2008/01/04 06:23:46 $"
__copyright__  = "Copyright (c) 2007-2008 Aaron Straup Cope. Perl Artistic License."

import re
import string
import urlparse

class validate :

    def __init__ (self) :

        self.re = {
            'coord' : re.compile(r"^-?\d+(?:\.\d+)?$"),
            'adjust' : re.compile(r"^(\d+(?:\.\d*)?|\d*?\.\d+)$"),
            'num' : re.compile(r"^\d+$"),
            'provider' : re.compile(r"^(GOOGLE|YAHOO|MICROSOFT)_(ROAD|HYBRID|AERIAL)$"),
            'label' : re.compile(r"^(?:[a-z0-9-_]+)$")
            }

    # ##########################################################
    
    def regexp (self, label, string) :

        if not self.re.has_key(label) :
            return False

        return self.re[label].match(string)

    # ##########################################################

    def ensure_args (self, args, required) :

        for i in required :

            if not args.has_key(i) :
                raise Exception, "Required argument %s missing" % i
            
        return True

    # ##########################################################
    
    def bbox (self, input) :

        bbox = input.split(",")
        
        if len(bbox) != 4 :
            raise Exception, "Missing or incomplete %s parameter" % 'bbox'
        
        bbox = map(string.strip, bbox)
        
        for pt in bbox :
            if not self.regexp('coord', pt) :
                raise Exception, "Not a valid lat/long : %s" % pt
            
        return map(float, bbox)

    # ##########################################################

    def bbox_adjustment (self, input) :

        if not self.regexp('adjust', str(input)) :
            raise Exception, "Not a valid adjustment %s " % input

        return float(input)
    
    # ##########################################################

    def latlon (self, input) :

        if not self.regexp('coord', input) :
            raise Exception, "Not a valid lat/long : %s" % input

        return float(input)

    # ##########################################################

    def zoom (self, input) :
        return self.__num(input)

    # ##########################################################

    def dimension (self, input) :
        return self.__num(input)

    # ##########################################################

    def provider (self, input) :

        input = input.upper()

        if not self.regexp('provider', input) :
            raise Exception, "Not a valid provider : %s" % p

        return input

    # ###########################################################
    
    def marker_label (self, input) :

        if not self.regexp('label', input) :
            raise Exception, "Not a valid marker label"

        return unicode(input)
    
    # ##########################################################

    def markers (self, markers) :

        valid = []

        for pos in markers :

            marker_data = {'width':75, 'height':75, 'adjust_cone_height' : 0}
            
            details = pos.split(",")
            details = map(string.strip, details)
            
            if len(details) < 3 :
                raise Exception, "Missing or incomplete %s parameter : %s" % ('marker', pos)

            #
            # Magic center/zoom markers
            #
            
            if details[0] == 'center' :

                marker_data['fill'] = 'center'
                marker_data['label'] = 'center'
                
                try : 
                    marker_data['provider'] = self.provider(details[1])
                except Exception, e :
                    raise Exception, e 

                try : 
                    marker_data['zoom'] = self.zoom(details[2])
                except Exception, e :
                    raise Exception, e 

            #
            # Pinwin name/label
            #
            
            else :
            
                try :
                    marker_data['label'] = self.marker_label(details[0])
                except Exception, e :
                    raise Exception, e

                # Pinwin location
            
                try :
                    marker_data['latitude'] = self.latlon(details[1])
                except Exception, e :
                    raise Exception, e

                try :
                    marker_data['longitude'] = self.latlon(details[2])
                except Exception, e :
                    raise Exception, e

            #
            # Shared
            #
            
            #
            # Pinwin size
            #
            
            if len(details) > 3 :

                if len(details) < 4 :
                    raise Exception, "Missing height parameter"
                
                try :
                    marker_data['width'] = self.dimension(details[3])
                except Exception, e :
                    raise Exception, e
                
                try : 
                    marker_data['height'] = self.dimension(details[4])
                except Exception, e :
                    raise Exception, e
            
            # URI for content to fill the pinwin with
            
            if len(details) > 5 :

                try :
                    parts = urlparse.urlparse(details[5])
                except Exception, e :
                    raise Exception, e

                if parts[1] == '' :
                    raise Exception, "Unknown URL"
                
                marker_data['fill'] = details[5]

            # Done

            valid.append(marker_data)

        return valid
    
    # ##########################################################
    
    def __num (self, input) :

        if not self.regexp('num', input) :
            raise Exception, "Not a valid number : %s" % p

        return int(input)

    # ##########################################################