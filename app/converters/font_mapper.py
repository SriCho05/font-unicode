"""
Font mapping module for converting non-Unicode Marathi fonts to Unicode
"""
import re

class FontMapper:
    def __init__(self):
        # DVTT Yogesh to Unicode mapping
        self.dvtt_yogesh_to_unicode = {
            # Consonants
            'd': 'क',
            'D': 'क',
            '[': 'ख',
            'k': 'ख',
            'x': 'ग',
            'g': 'ग',
            '?': 'घ',
            'G': 'घ',
            'p': 'च',
            'c': 'च',
            'P': 'छ',
            'C': 'छ',
            'h': 'ज',
            'j': 'ज',
            'H': 'झ',
            'J': 'झ',
            'V': 'ट',
            'T': 'ट',
            'B': 'ठ',
            '<': 'ढ',
            'l': 'त',
            't': 'त',
            'L': 'थ',
            'n': 'द',
            'N': 'ध',
            'u': 'न',
            'i': 'प',
            'I': 'फ',
            'f': 'फ',
            'c': 'ब',
            'C': 'भ',
            'e': 'म',
            'm': 'म',
            'j': 'य',
            'y': 'य',
            'r': 'र',
            'v': 'ल',
            'o': 'व',
            ';': 'श',
            '"': 'ष',
            's': 'स',
            'g': 'ह',
            
            # Vowels
            'v': 'अ',
            'vk': 'आ',
            'b': 'इ',
            'bZ': 'ई',
            'w': 'उ',
            'wZ': 'ऊ',
            's': 'ए',
            'sZ': 'ऐ',
            'ks': 'ओ',
            'kS': 'औ',
            
            # Vowel signs (matras)
            'k': 'ा',
            'h': 'ि',
            'Z': 'ी',
            'q': 'ु',
            'Q': 'ू',
            's': 'े',
            'sZ': 'ै',
            'ks': 'ो',
            'kS': 'ौ',
            
            # Special characters
            '`': '्',  # Halant (virama)
            'a': 'ं',  # Anusvara
            'W': 'ः',  # Visarga
            '।': '।',  # Devanagari danda
            '॥': '॥', # Double danda
        }
        
        # DTT Dhruv to Unicode mapping
        self.dtt_dhruv_to_unicode = {
            # Consonants
            'd': 'क',
            '[': 'ख',
            'x': 'ग',
            '?': 'घ',
            'p': 'च',
            'P': 'छ',
            'h': 'ज',
            'H': 'झ',
            'V': 'ट',
            'B': 'ठ',
            'M': 'ड',
            '<': 'ढ',
            'l': 'त',
            'L': 'थ',
            'n': 'द',
            'N': 'ध',
            'u': 'न',
            'i': 'प',
            'I': 'फ',
            'c': 'ब',
            'C': 'भ',
            'e': 'म',
            'j': 'य',
            'r': 'र',
            'v': 'ल',
            'o': 'व',
            ';': 'श',
            '"': 'ष',
            's': 'स',
            'g': 'ह',
            
            # Vowels  
            'v': 'अ',
            'vk': 'आ',
            'b': 'इ',
            'bZ': 'ई',
            'w': 'उ',
            'wZ': 'ऊ',
            's': 'ए',
            'sZ': 'ऐ',
            'ks': 'ओ',
            'kS': 'औ',
            
            # Vowel signs
            'k': 'ा',
            'h': 'ि',
            'Z': 'ी', 
            'q': 'ु',
            'Q': 'ू',
            's': 'े',
            'sZ': 'ै',
            'ks': 'ो',
            'kS': 'ौ',
            
            # Special characters
            '`': '्',
            'a': 'ं',
            'W': 'ः',
            '।': '।',
            '॥': '॥',
        }
        
        # Create reverse mappings for detection
        self.unicode_to_dvtt_yogesh = {v: k for k, v in self.dvtt_yogesh_to_unicode.items()}
        self.unicode_to_dtt_dhruv = {v: k for k, v in self.dtt_dhruv_to_unicode.items()}
        
        # Compile patterns for efficient replacement
        self._compile_replacement_patterns()
    
    def _compile_replacement_patterns(self):
        """Compile regex patterns for efficient text replacement"""
        # Sort by length (longest first) to handle multi-character mappings properly
        dvtt_keys = sorted(self.dvtt_yogesh_to_unicode.keys(), key=len, reverse=True)
        dtt_keys = sorted(self.dtt_dhruv_to_unicode.keys(), key=len, reverse=True)
        
        # Escape special regex characters
        dvtt_pattern = '|'.join(re.escape(key) for key in dvtt_keys)
        dtt_pattern = '|'.join(re.escape(key) for key in dtt_keys)
        
        self.dvtt_pattern = re.compile(dvtt_pattern)
        self.dtt_pattern = re.compile(dtt_pattern)
    
    def convert_dvtt_yogesh_to_unicode(self, text):
        """
        Convert DVTT Yogesh font text to Unicode Marathi
        
        Args:
            text (str): Input text in DVTT Yogesh font
            
        Returns:
            str: Converted Unicode Marathi text
        """
        def replace_match(match):
            matched_text = match.group(0)
            return self.dvtt_yogesh_to_unicode.get(matched_text, matched_text)
        
        return self.dvtt_pattern.sub(replace_match, text)
    
    def convert_dtt_dhruv_to_unicode(self, text):
        """
        Convert DTT Dhruv font text to Unicode Marathi
        
        Args:
            text (str): Input text in DTT Dhruv font
            
        Returns:
            str: Converted Unicode Marathi text
        """
        def replace_match(match):
            matched_text = match.group(0)
            return self.dtt_dhruv_to_unicode.get(matched_text, matched_text)
        
        return self.dtt_pattern.sub(replace_match, text)
    
    def convert_text(self, text, source_font='auto'):
        """
        Convert non-Unicode Marathi text to Unicode
        
        Args:
            text (str): Input text to convert
            source_font (str): Source font type ('dvtt_yogesh', 'dtt_dhruv', 'auto')
            
        Returns:
            str: Converted Unicode text
        """
        if not text:
            return text
        
        # Auto-detect source font if not specified
        if source_font == 'auto':
            from .font_detector import FontDetector
            detector = FontDetector()
            detection = detector.detect_fonts(text)
            
            if detection['dvtt_yogesh']['detected']:
                source_font = 'dvtt_yogesh'
            elif detection['dtt_dhruv']['detected']:
                source_font = 'dtt_dhruv'
            else:
                # Return original text if no non-Unicode fonts detected
                return text
        
        # Convert based on detected/specified font
        if source_font == 'dvtt_yogesh':
            return self.convert_dvtt_yogesh_to_unicode(text)
        elif source_font == 'dtt_dhruv':
            return self.convert_dtt_dhruv_to_unicode(text)
        else:
            return text
    
    def convert_with_preservation(self, text, preserve_english=True, preserve_numbers=True):
        """
        Convert text while preserving English and numbers
        
        Args:
            text (str): Input text to convert
            preserve_english (bool): Whether to preserve English text
            preserve_numbers (bool): Whether to preserve numbers
            
        Returns:
            str: Converted text with preserved elements
        """
        if not text:
            return text
        
        # Split text into segments
        segments = []
        current_pos = 0
        
        # Find English text segments if preservation is enabled
        if preserve_english:
            english_pattern = re.compile(r'[a-zA-Z\s]+')
            for match in english_pattern.finditer(text):
                # Add non-English text before this English segment
                if match.start() > current_pos:
                    marathi_segment = text[current_pos:match.start()]
                    segments.append(('marathi', marathi_segment))
                
                # Add English segment
                segments.append(('english', match.group()))
                current_pos = match.end()
        
        # Add remaining text
        if current_pos < len(text):
            segments.append(('marathi', text[current_pos:]))
        
        # If no English text found, treat entire text as Marathi
        if not segments:
            segments = [('marathi', text)]
        
        # Convert each segment appropriately
        converted_segments = []
        for segment_type, segment_text in segments:
            if segment_type == 'marathi':
                converted_segments.append(self.convert_text(segment_text))
            else:
                converted_segments.append(segment_text)
        
        return ''.join(converted_segments)
    
    def get_conversion_stats(self, original_text, converted_text):
        """
        Generate statistics about the conversion
        
        Args:
            original_text (str): Original text
            converted_text (str): Converted text
            
        Returns:
            dict: Conversion statistics
        """
        from .font_detector import FontDetector
        detector = FontDetector()
        
        original_detection = detector.detect_fonts(original_text)
        converted_detection = detector.detect_fonts(converted_text)
        
        stats = {
            'original_length': len(original_text),
            'converted_length': len(converted_text),
            'original_fonts': [],
            'converted_fonts': [],
            'conversion_ratio': 0.0
        }
        
        # Find detected fonts in original text
        for font_type, info in original_detection.items():
            if info['detected']:
                stats['original_fonts'].append(font_type)
        
        # Find detected fonts in converted text
        for font_type, info in converted_detection.items():
            if info['detected']:
                stats['converted_fonts'].append(font_type)
        
        # Calculate conversion ratio
        if stats['original_length'] > 0:
            stats['conversion_ratio'] = abs(stats['converted_length'] - stats['original_length']) / stats['original_length']
        
        return stats