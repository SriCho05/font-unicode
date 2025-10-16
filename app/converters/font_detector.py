"""
Font detection module for identifying non-Unicode Marathi fonts
"""
import re
import unicodedata

class FontDetector:
    def __init__(self):
        # Character patterns for DVTT Yogesh font
        self.dvtt_yogesh_patterns = {
            # Common DVTT Yogesh character mappings
            'क': ['d', 'D'],
            'ख': ['[', 'k'],
            'ग': ['x', 'g'],
            'घ': ['?', 'G'],
            'च': ['p', 'c'],
            'छ': ['P', 'C'],
            'ज': ['h', 'j'],
            'झ': ['H', 'J'],
            'ट': ['V', 'T'],
            'ठ': ['B', 'Th'],
            'ड': ['M', 'D'],
            'ढ': ['<', 'Dh'],
            'त': ['l', 't'],
            'थ': ['L', 'th'],
            'द': ['n', 'da'],
            'ध': ['N', 'dh'],
            'न': ['u', 'n'],
            'प': ['i', 'p'],
            'फ': ['I', 'f'],
            'ब': ['c', 'b'],
            'भ': ['C', 'bh'],
            'म': ['e', 'm'],
            'य': ['j', 'y'],
            'र': ['j', 'r'],
            'ल': ['v', 'l'],
            'व': ['o', 'v'],
            'श': [';', 'sh'],
            'ष': ['\"', 'Sh'],
            'स': ['l', 's'],
            'ह': ['g', 'h'],
            'अ': ['v', 'a'],
            'आ': ['vk', 'aa'],
            'इ': ['b', 'i'],
            'ई': ['bZ', 'ii'],
            'उ': ['w', 'u'],
            'ऊ': ['wZ', 'uu'],
            'ए': ['s', 'e'],
            'ऐ': ['sZ', 'ai'],
            'ओ': ['ks', 'o'],
            'औ': ['kS', 'au']
        }
        
        # Character patterns for DTT Dhruv font
        self.dtt_dhruv_patterns = {
            'क': ['d', 'क़'],
            'ख': ['[', 'ख़'], 
            'ग': ['x', 'ग़'],
            'घ': ['?', 'घ़'],
            'च': ['p', 'च़'],
            'छ': ['P', 'छ़'],
            'ज': ['h', 'ज़'],
            'झ': ['H', 'झ़'],
            'ट': ['V', 'ट़'],
            'ठ': ['B', 'ठ़'],
            'ड': ['M', 'ड़'],
            'ढ': ['<', 'ढ़'],
            'त': ['l', 'त़'],
            'थ': ['L', 'थ़'],
            'द': ['n', 'द़'],
            'ध': ['N', 'ध़'],
            'न': ['u', 'ऩ'],
            'प': ['i', 'प़'],
            'फ': ['I', 'फ़'],
            'ब': ['c', 'ब़'],
            'भ': ['C', 'भ़'],
            'म': ['e', 'म़'],
            'य': ['j', 'य़'],
            'र': ['j', 'ऱ'],
            'ल': ['v', 'ल़'],
            'व': ['o', 'व़'],
            'श': [';', 'श़'],
            'ष': ['\"', 'ष़'],
            'स': ['l', 'स़'],
            'ह': ['g', 'ह़']
        }
        
        # Compile regex patterns for efficient detection
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Compile regex patterns for font detection"""
        # DVTT Yogesh detection patterns
        dvtt_chars = []
        for unicode_char, non_unicode_list in self.dvtt_yogesh_patterns.items():
            dvtt_chars.extend(non_unicode_list)
        
        # DTT Dhruv detection patterns  
        dtt_chars = []
        for unicode_char, non_unicode_list in self.dtt_dhruv_patterns.items():
            dtt_chars.extend(non_unicode_list)
        
        # Create regex patterns
        self.dvtt_pattern = re.compile(r'[' + re.escape(''.join(dvtt_chars)) + r']+')
        self.dtt_pattern = re.compile(r'[' + re.escape(''.join(dtt_chars)) + r']+')
    
    def detect_fonts(self, text):
        """
        Detect which non-Unicode fonts are present in the text
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            dict: Detection results with font types and confidence scores
        """
        results = {
            'dvtt_yogesh': {
                'detected': False,
                'confidence': 0.0,
                'matches': []
            },
            'dtt_dhruv': {
                'detected': False,
                'confidence': 0.0,
                'matches': []
            },
            'unicode_marathi': {
                'detected': False,
                'confidence': 0.0,
                'matches': []
            },
            'english': {
                'detected': False,
                'confidence': 0.0,
                'matches': []
            }
        }
        
        if not text:
            return results
        
        # Check for DVTT Yogesh patterns
        dvtt_matches = self.dvtt_pattern.findall(text)
        if dvtt_matches:
            results['dvtt_yogesh']['detected'] = True
            results['dvtt_yogesh']['matches'] = dvtt_matches
            results['dvtt_yogesh']['confidence'] = min(len(dvtt_matches) / 10.0, 1.0)
        
        # Check for DTT Dhruv patterns
        dtt_matches = self.dtt_pattern.findall(text)
        if dtt_matches:
            results['dtt_dhruv']['detected'] = True
            results['dtt_dhruv']['matches'] = dtt_matches
            results['dtt_dhruv']['confidence'] = min(len(dtt_matches) / 10.0, 1.0)
        
        # Check for Unicode Marathi (Devanagari script)
        unicode_marathi = re.findall(r'[\u0900-\u097F]+', text)
        if unicode_marathi:
            results['unicode_marathi']['detected'] = True
            results['unicode_marathi']['matches'] = unicode_marathi
            results['unicode_marathi']['confidence'] = min(len(unicode_marathi) / 10.0, 1.0)
        
        # Check for English text
        english_text = re.findall(r'[a-zA-Z]+', text)
        if english_text:
            results['english']['detected'] = True
            results['english']['matches'] = english_text
            results['english']['confidence'] = min(len(english_text) / 10.0, 1.0)
        
        return results
    
    def is_non_unicode_marathi(self, text):
        """
        Check if text contains non-Unicode Marathi fonts
        
        Args:
            text (str): Input text to check
            
        Returns:
            bool: True if non-Unicode Marathi fonts are detected
        """
        detection = self.detect_fonts(text)
        return (detection['dvtt_yogesh']['detected'] or 
                detection['dtt_dhruv']['detected'])
    
    def get_dominant_font(self, text):
        """
        Determine the dominant font type in the text
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            str: Name of the dominant font type
        """
        detection = self.detect_fonts(text)
        
        # Find font with highest confidence
        max_confidence = 0
        dominant_font = 'unknown'
        
        for font_type, info in detection.items():
            if info['confidence'] > max_confidence:
                max_confidence = info['confidence']
                dominant_font = font_type
        
        return dominant_font if max_confidence > 0.1 else 'unknown'