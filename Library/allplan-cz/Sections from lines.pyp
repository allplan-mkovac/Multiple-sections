<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>allplan-cz\SectionsFromLines.py</Name>
        <Title>Sklopené řezy z čar</Title>
        <TextId>1001</TextId>
        <Interactor>False</Interactor>
        <Version>0.1.0</Version>
        <ShowFavoriteButtons>True</ShowFavoriteButtons>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Page>
        <Name>Create multiple sections</Name>
        <Text>Create multiple sections from lines</Text>

            <Parameter>
                <Name>NameRow</Name>
                <Text>Návod na použití</Text>
                <TextId>1012</TextId>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>InfoPicture</Name>
                    <Text>
1) Nakreslete 2D čáry v místech kde potřebujete vytvořit řezy
2) Vyberte v pluginu hladinu, ve které jsou 2D čáry nakreslené
3) Tlačítkem vytvořte řezy, případně vytvořte řezy a vymažte čáry
4) Řezy budou očíslovány postupně, počínaje číslem zadaným v poli "Číslo prvního řezu"
5) Volba "Zohlednit směr čáry" umožní vytvořit řezy s ohledem na směr čáry, jinak jsou vygenrovány vždy "zdola a zprava"
Pozn.
    Řezy budou vytvořeny v aktuální fólii.
    V řezech budou viditelné všechny zapnuté fólie (i pasivní).
                    </Text>
                    <TextId>1050</TextId>
                    <Value>AllplanSettings.PictResPalette.eHotinfo</Value>
                    <ValueType>Picture</ValueType>
                </Parameter>

            </Parameter>

            <Parameter>
                <Name>Separator</Name>
                <ValueType>Separator</ValueType>
            </Parameter>

            <Parameter>
                <Name>section_depth</Name>
                <Text>Hloubka řezu</Text>
                <TextId>1002</TextId>
                <Value>200</Value>
                <ValueType>Length</ValueType>
            </Parameter>

            <Parameter>
                <Name>section_top</Name>
                <Text>Horní hrana řezů</Text>
                <TextId>1003</TextId>
                <Value>3500</Value>
                <ValueType>Length</ValueType>
            </Parameter>

            <Parameter>
                <Name>section_bottom</Name>
                <Text>Dolní hrana řezů</Text>
                <TextId>1004</TextId>
                <Value>2500</Value>
                <ValueType>Length</ValueType>
            </Parameter>

            <Parameter>
                <Name>layer_filter</Name>
                <Text>Hladina čar</Text>
                <TextId>1005</TextId>
                <Value></Value>
                <ValueType>Layer</ValueType>
            </Parameter>

            <Parameter>
                <Name>direction</Name>
                <Text>Zohlednit směr čáry</Text>
                <TextId>1006</TextId>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>first_no</Name>
                <Text>Číslo prvního řezu</Text>
                <TextId>1007</TextId>
                <Value>1</Value>
                <MinValue>1</MinValue>
                <ValueType>Integer</ValueType>
            </Parameter>

            <Parameter>
                <Name>Row1</Name>
                <Text>Vytvořit řezy</Text>
                <TextId>1008</TextId>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>Button1</Name>
                    <Text>Vytvoř</Text>
                    <TextId>1009</TextId>
                    <EventId>1000</EventId>
                    <Value>9025</Value>
                    <ValueType>PictureResourceButton</ValueType>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>Row2</Name>
                <Text>Vytvořit řezy a vymazat čáry</Text>
                <TextId>1010</TextId>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>Button2</Name>
                    <Text>Vytvoř a vymaž</Text>
                    <TextId>1011</TextId>
                    <EventId>1001</EventId>
                    <Value>9025</Value>
                    <ValueType>PictureResourceButton</ValueType>
                </Parameter>
            </Parameter>

    </Page>
</Element>
