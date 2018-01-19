/**
 * File of functions to be added to cwl files
 */

function generateGATK4BooleanValue(){
    /**
     * Boolean types in GATK 4 are expressed on the command line as --<PREFIX> "true"/"false",
     * so patch here
     */
    if(self === true || self === false){
        return self.toString()
    }

    return self;
}

function applyTagsToArgument(prefix, tags){
    /**
     * Function to be used in the field valueFrom of File objects to add gatk tags.
     */

    if(!self){
        return null;
    }
    else if(!tags){
        return generateArrayCmd(prefix);
    }
    else{
        function addTagToArgument(tagObject, argument){
            var allTags = Array.isArray(tagObject) ? tagObject.join(",") : tagObject;

            return [prefix + ":" + allTags, argument];
        }

        if(Array.isArray(self)){
            if(!Array.isArray(tags) || self.length !== tags.length){
                throw new TypeError("Argument '" + prefix + "' tag field is invalid");
            }

            var value = self.map(function(element, i) {
                return addTagToArgument(tags[i], element);
            }).reduce(function(a, b){return a.concat(b)})

            return value;
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
    if(!self){
        return null;
    }

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