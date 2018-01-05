/**
 * File of functions to be added to cwl files
 * NOTE: for easy minification, single line comments are not
 * allowed and every statement has to be terminated by a semicolon
 */
function applyTagsToArgument(prefix, tags){
    /**
     * Function to be used in the field valueFrom of File objects to add gatk tags.
     */
    if(!self){
        return null;
    }
    else if(!tags){
        return [prefix, self];
    }
    else{
        function addTagToArgument(tagObject, argument){
            var allTags = Array.isArray(tagObject) ? tagObject.join(",") : tagObject;

            return [prefix + ":" + allTags, self];
        }

        if(Array.isArray(self)){
            if(!Array.isArray(tags) || self.length !== tags.length){
                throw new TypeError("Argument '" + prefix + "' tag field is invalid");
            }

            return self.map(function(element, i) {
                return addTagToArgument(tags, element);
            })
        }
        else{
            return addTagToArgument(tags, self);
        }
    }
}

function generateArrayCmd(prefix){
    /**
     * Function to be used in the field valueFrom of array objects, so that arrays are optional
     * and prefixes are handled properly.
     *
     * The issue that this solves is documented here:
     * https://www.biostars.org/p/258414/#260140
     */
    if(!Array.isArray(self)){
        self = [self];
    }

    var output = [];
    self.forEach(function(element) {
        output.push(prefix);
        output.push(element);
    })

    return output;
}